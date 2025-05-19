from django.contrib.auth import get_user_model, authenticate
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from rest_framework import serializers
from rest_framework.authtoken.models import Token


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model."""

    confirm_password = serializers.CharField(
        max_length=250, write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = get_user_model()
        fields = (
            "email",
            "first_name",
            "last_name",
            "date_joined",
            "date_updated",
            "password",
            "confirm_password",
            "is_staff",
            "is_active",
            "is_verified",
        )
        extra_kwargs = {
            "date_joined": {"read_only": True},
            "date_updated": {"read_only": True},
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "is_active": {"read_only": True},
            "is_staff": {"read_only": True},
            "is_verified": {"read_only": True},
        }

    def validate(self, attrs):

        password = attrs.get("password")
        confirm_password = attrs.pop("confirm_password")

        if password != confirm_password:
            raise ValidationError(_("Passwords didn't match"))

        return attrs

    def create(self, validated_data):
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        user = get_user_model().objects.get(email=validated_data["email"])

        user.set_password(validated_data["password"])
        user.save()

        validated_data["password"] = user.password

        return super().update(instance, validated_data)


class UpdateUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("id", "first_name", "last_name", "email", "is_staff", "is_verified")

    def update(self, instance, validated_data):
        return super().update(instance, validated_data)


class UpdateUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = get_user_model()
        fields = ("first_name", "last_name", "email", "is_verified", "is_active")
        extra_kwargs = {
            "email": {"read_only": True},
            "is_verified": {"read_only": True},
            "is_active": {"read_only": True},
        }


class SendPasswordResetLinkSerializer(serializers.Serializer):
    """Serializer for sending password reset link."""

    email = serializers.EmailField()


class PasswordResetSerializer(serializers.Serializer):
    """Serializer for password reset"""

    password = serializers.CharField(
        min_length=6, max_length=70, write_only=True, style={"input_type": "password"}
    )
    confirm_password = serializers.CharField(style={"input_type": "password"})

    class Meta:
        fields = ["password", "confirm_password"]

    def validate(self, attrs):

        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password != confirm_password:
            raise ValidationError(_("Passwords did not match"))

        return super().validate(attrs)


class SendEmailVerificationSerializer(serializers.Serializer):
    """Serializer for sending an email verification email."""

    email = serializers.EmailField()


class EmailVerificationSerializer(serializers.Serializer):
    """Serializer for verifying the emails."""

    token = serializers.CharField(trim_whitespace=True)


class TokenVerificationSerializer(serializers.Serializer):
    """Serializer for verifying the authentication tokens."""

    token = serializers.CharField(trim_whitespace=True)

    def validate_token(self, token_key):
        try:
            token = Token.objects.get(key=token_key)

            return token.user
        except Token.DoesNotExist:
            msg = _("Invalid token")
            raise ValidationError(msg, code="invalid_token")


class AuthTokenSerializer(serializers.Serializer):
    """Serializer for creating authentication token."""

    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False,
    )

    def validate(self, attrs):

        email = attrs.get("email")
        password = attrs.get("password")

        user = authenticate(
            request=self.context.get("request"), username=email, password=password
        )

        if not user:
            msg = _("Validation Error, invalid credentials")
            raise serializers.ValidationError(msg, code="authentication")

        if not user.is_active:
            msg = _("User is blocked, please contact the admin")
            raise ValidationError(msg, code="not_active")

        if not user.is_verified:
            msg = _("Email is not verified, please verify your email")
            raise ValidationError(msg, code="not_verified")

        attrs["user"] = user

        return attrs
