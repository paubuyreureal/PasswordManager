from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Account

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        try:
            user = User.objects.create_user(**validated_data)
            return user
        except Exception as e:
            if 'username' in str(e) or 'UNIQUE constraint failed' in str(e):
                raise serializers.ValidationError({
                    'username': ['A user with this username already exists. Please choose a different username.']
                })
            raise serializers.ValidationError({
                'non_field_errors': ['Registration failed. Please try again.']
            })

class AccountSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)  # Only for input
    decrypted_password = serializers.SerializerMethodField()  # For output
    favicon_url = serializers.SerializerMethodField()  # For output

    class Meta:
        model = Account
        fields = ["id", "username", "password", "decrypted_password", "url", "notes", "icon", "favicon_url", "created_at", "author"]
        extra_kwargs = {"author": {"read_only": True}}

    def get_decrypted_password(self, obj):
        """Return decrypted password for the authenticated user"""
        try:
            return obj.get_password()
        except Exception:
            return "Error decrypting password"

    def get_favicon_url(self, obj):
        """Return the favicon URL (cached or manual icon)"""
        return obj.get_favicon_url()

    def create(self, validated_data):
        """Create account with encrypted password"""
        password = validated_data.pop('password')
        account = Account.objects.create(**validated_data)
        try:
            account.set_password(password)
            account.save()
        except Exception as e:
            account.delete()
            raise serializers.ValidationError(f"Failed to encrypt password: {str(e)}")
        return account