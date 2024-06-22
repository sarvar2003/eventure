from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    """Serializer for User model"""

    confirm_password = serializers.CharField(max_length=250, write_only=True, style={'input_type': 'password'})

    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name', 'password', 'confirm_password', 'date_joined', 'date_updated', 'is_staff', 'is_active', 'is_verified' )
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
            'date_joined': {'read_only': True},
            'date_updated': {'read_only': True},
            'is_staff': {'read_only': True},
            'is_active': {'read_only': True},
            'is_verified': {'read_only': True},
        }
    
    def validate(self, attrs):

        password = attrs.get('password')
        confirm_password = attrs.pop('confirm_password')

        if password != confirm_password:
            raise ValidationError(_('Passwords did not match'))

        return attrs
    
    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)
    

class VerifyEmailSerializer(serializers.Serializer):

    """Serializer for verifying user email"""

    token = serializers.CharField(read_only=True)


class UpdateUserSerializer(serializers.ModelSerializer):

    """Serializer for updating user details"""

    class Meta:
        model = get_user_model()
        fields = ('id', 'email', 'first_name', 'last_name', 'is_verified', 'is_staff')


class SendResetLinkSerializer(serializers.Serializer):

    """Serializer for sending password reset link"""

    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):

    """Serializer for password reset"""

    password = serializers.CharField(max_length=250, style={'input_type': 'password'})
    confirm_password = serializers.CharField(max_length=250, style={'input_type': 'password'})

    def validate(self, attrs):
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')

        if password != confirm_password:
            raise ValidationError(_('Passwords did not match'))
        
        return attrs


class VerifyTokenSerializer(serializers.Serializer):

    """Serializer for token verification"""

    token = serializers.CharField()


class AuthTokenSerializer(serializers.Serializer):

    """Serializer for obtaining auth token"""

    email = serializers.EmailField()
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)

        if not user:
            raise ValidationError(_('Invalid credentials'))

        if not user.is_active:
            raise ValidationError(_('User has is not activated, please contact admin')) 
        
        if not user.is_verified:
            raise ValidationError(_('User is not verified, please verify email'))
        
        attrs['user'] = user

        return attrs