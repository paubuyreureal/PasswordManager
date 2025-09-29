from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for requesting a password reset e-mail"""
    username = serializers.CharField()

    def validate_username(self, value):
        """Validate that the username exists and has an email"""
        try:
            user = User.objects.get(username=value)
            if not user.email:
                raise serializers.ValidationError(
                    _("No email address associated with this username.")
                )
        except User.DoesNotExist:
            raise serializers.ValidationError(
                _("No account found with this username.")
            )
        return value

    def save(self):
        """Generate a one-use only link for resetting password and send it to the user"""
        request = self.context.get('request')
        username = self.validated_data['username']

        user = User.objects.get(username=username)
        from django.contrib.auth.tokens import default_token_generator
        from django.utils.http import urlsafe_base64_encode
        from django.utils.encoding import force_bytes

        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        
        # For Docker deployment, explicitly use localhost:3000 for frontend
        frontend_host = "localhost:3000"
        reset_link = f"{request.scheme}://{frontend_host}/reset-password/{uid}-{token}"

        form = PasswordResetForm({'email': user.email})
        if form.is_valid():
            form.save(
                request=request,
                use_https=request.is_secure(),
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL'),
                email_template_name='registration/password_reset_email.html',
                subject_template_name='registration/password_reset_subject.txt',
                extra_email_context={'reset_link': reset_link}
            )


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer for confirming a password reset attempt"""
    new_password1 = serializers.CharField(max_length=128)
    new_password2 = serializers.CharField(max_length=128)
    uid = serializers.CharField()
    token = serializers.CharField()

    def validate(self, attrs):
        """Validate that the two password entries match"""
        if attrs['new_password1'] != attrs['new_password2']:
            raise serializers.ValidationError(
                _("The two password fields didn't match."))
        return attrs

    def validate_new_password1(self, value):
        """Validate the new password strength"""
        from django.contrib.auth.password_validation import validate_password
        from django.core.exceptions import ValidationError

        try:
            validate_password(value)
        except ValidationError as e:
            raise serializers.ValidationError(e.messages)
        return value
