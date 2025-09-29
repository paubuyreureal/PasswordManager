from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.contrib.auth.forms import SetPasswordForm
from .password_reset_serializers import PasswordResetSerializer, PasswordResetConfirmSerializer

User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    """Request a password reset email"""
    serializer = PasswordResetSerializer(data=request.data, context={'request': request})
    
    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                'message': 'Password reset email sent successfully. Please check your email for further instructions.',
                'username': serializer.validated_data['username']
            },
            status=status.HTTP_200_OK
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request):
    """Confirm password reset with token"""
    token = request.data.get('token')
    password = request.data.get('password')
    
    if not token or not password:
        return Response(
            {'error': 'Token and password are required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    
    try:
        # Decode the user ID from token (split only on first hyphen)
        parts = token.split('-', 1)
        if len(parts) != 2:
            raise ValueError("Invalid token format")
        uid = force_str(urlsafe_base64_decode(parts[0]))
        user = User.objects.get(pk=uid)
        actual_token = parts[1]
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, IndexError):
        return Response(
            {'error': 'Invalid reset link. Please request a new password reset.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Verify the token
    if not default_token_generator.check_token(user, actual_token):
        return Response(
            {'error': 'Invalid or expired reset link. Please request a new password reset.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    # Set the new password
    user.set_password(password)
    user.save()
    
    return Response(
        {
            'message': 'Password reset successfully. You can now log in with your new password.',
            'username': user.username
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_validate_token(request):
    """Validate if a password reset token is valid"""
    token = request.data.get('token')
    
    if not token:
        return Response(
            {'error': 'Token is required.'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        # Decode the user ID from token (split only on first hyphen)
        parts = token.split('-', 1)
        if len(parts) != 2:
            raise ValueError("Invalid token format")
        uid = force_str(urlsafe_base64_decode(parts[0]))
        user = User.objects.get(pk=uid)
        actual_token = parts[1]
    except (TypeError, ValueError, OverflowError, User.DoesNotExist, IndexError):
        return Response(
            {'valid': False, 'error': 'Invalid reset link.'},
            status=status.HTTP_200_OK
        )
    
    # Verify the token
    if default_token_generator.check_token(user, actual_token):
        return Response(
            {
                'valid': True,
                'message': 'Token is valid.',
                'username': user.username
            },
            status=status.HTTP_200_OK
        )
    else:
        return Response(
            {
                'valid': False,
                'error': 'Invalid or expired reset link.'
            },
            status=status.HTTP_200_OK
        )
