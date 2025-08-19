from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string
from django.shortcuts import get_object_or_404

from rest_framework import generics, permissions, views, status
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.settings import api_settings
from rest_framework.parsers import JSONParser

from core import custom_permission
from users import serializers

from core import utils


class AllUsers(generics.ListAPIView):
    """API View for listing all available users."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all()


class UserAPIView(generics.CreateAPIView):
    """API View for creating users."""

    parser_classes = (JSONParser,)
    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.UserSerializer

    def post(self, request, *args, **kwargs):

        user = request.data

        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data

        user = get_user_model().objects.get(email=user_data["email"])
        token, _ = Token.objects.get_or_create(user=user)
        frontend_base_url = "http://localhost:5173"
        reset_path = f"/verify-email/{token}"
        absolute_url = frontend_base_url + reset_path
        email_body = "Plase use the link below to verify your email\n" + absolute_url
        html_message = render_to_string(
            "email_verification_page.html",
            context={"first_name": user.first_name, "absolute_url": absolute_url},
        )

        data = {
            "email_body": email_body,
            "to_email": user.email,
            "email_subject": "Verify your email - Eventure",
            "html_message": html_message,
        }
        utils.SendEmailUtil.send_mail(data)

        return Response(
            {"status": "Verify your email", "user": user_data},
            status=status.HTTP_201_CREATED,
        )


class CurrentUserAPIView(generics.RetrieveDestroyAPIView):
    """Retrieve the currently authenticated user."""

    serializer_class = serializers.UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), email=request.user.email)
        serializer = self.serializer_class(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), email=request.user.email)
        user.delete()
        return Response(
            {"status": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


class UpdateUserAPIView(generics.RetrieveUpdateAPIView):
    """API View for updating the user."""

    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UpdateUserSerializer
    parser_classes = (JSONParser,)

    def post(self, request, *args, **kwargs):
        email = kwargs.get("email")
        if email:
            user = get_object_or_404(get_user_model(), email=email)
            serializer = self.serializer_class(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)


class SendPasswordResetEmailAPIView(views.APIView):
    """API View for sending password reset link."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.SendPasswordResetLinkSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]

        try:
            user = get_user_model().objects.get(email=email)

            token, _ = Token.objects.get_or_create(user=user)
            frontend_base_url = "http://localhost:5173"
            reset_path = f"/password-reset/{token}"
            absolute_url = frontend_base_url + reset_path
            email_body = f"Hello, {user.first_name}! \nPlease use the link below to reset your password for your Eventure account.\n{absolute_url}"
            html_message = render_to_string(
                "password_reset_email_page.html",
                context={"first_name": user.first_name, "absolute_url": absolute_url},
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Password Reset - Eventure",
                "html_message": html_message,
            }
            utils.SendEmailUtil.send_mail(data)

            return Response({"status": "Email sent, please check your email"})

        except get_user_model().DoesNotExist:

            return Response({"status": f"Email {email} does not exist in our system"})


class PasswordResetAPIView(views.APIView):
    """API View to reset the user password."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.PasswordResetSerializer

    def get(self, request, token):

        try:
            user_token = Token.objects.get(key=token)

            try:
                get_user_model().objects.get(id=user_token.user.id)

                return Response({"status": "valid"})

            except get_user_model().DoesNotExist:
                return Response(
                    {
                        "status": "Invalid token, requested user no longer exists, user might have been deleted. Plase contact our customer support"
                    }
                )

        except Token.DoesNotExist:
            return Response(
                {"status": "Invalid token, please try again"},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def post(self, request, token):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        new_password = serializer.data["confirm_password"]

        user_token = Token.objects.get(key=token)

        user = get_user_model().objects.get(id=user_token.user.id)

        user.set_password(new_password)

        user.save()

        return Response(
            {"status": "Password reset successfully"}, status=status.HTTP_200_OK
        )


class SendVerificationEmail(views.APIView):
    """API View for sending verification email."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.SendEmailVerificationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        email = serializer.data["email"]

        try:
            user = get_user_model().objects.get(email=email)

            token, _ = Token.objects.get_or_create(user=user)
            current_site = get_current_site(request).domain
            relative_link = reverse("users:email-verify", kwargs={"token": token})
            absolute_url = "http://" + current_site + relative_link
            email_body = f"Hello from Eventure!\nPlease use the link below to verify your email\n{absolute_url}"
            html_message = render_to_string(
                "email_verification_page.html",
                context={"first_name": user.first_name, "absolute_url": absolute_url},
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "Verify your email - Eventure",
                "html_message": html_message,
            }
            utils.SendEmailUtil.send_mail(data)

            return Response({"status": "Email sent, please check your email"})

        except get_user_model().DoesNotExist:

            return Response({"status": f"Email {email} does not exist in our system"})


class VerifyEmail(views.APIView):
    """API View for verifying the email."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.EmailVerificationSerializer

    def get(self, request, token):

        try:
            user_token = Token.objects.get(key=token)

            user = get_user_model().objects.get(id=user_token.user.id)

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {
                    "status": "Email is verified",
                    "user": {
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                        "is_verified": user.is_verified,
                    },
                }
            )

        except Token.DoesNotExist:
            return Response({"status": "Token is not valid"})


class VerifyToken(views.APIView):
    """API View for verifying the authentication tokens."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.TokenVerificationSerializer

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            # Token is valid
            user = serializer.validated_data["token"]

            return Response(
                {
                    "token": Token.objects.get(user=user).key,
                    "user_id": user.pk,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "date_joined": {
                        "year": user.date_joined.year,
                        "month": user.date_joined.month,
                        "day": user.date_joined.day,
                        "time": user.date_joined.time().strftime("%H:%M:%S"),
                    },
                    "date_updated": {
                        "year": user.date_updated.year,
                        "month": user.date_updated.month,
                        "day": user.date_updated.day,
                        "time": user.date_updated.time().strftime("%H:%M:%S"),
                    },
                }
            )
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AuthTokenAPIView(ObtainAuthToken):
    """API View for obtaining authentication token."""

    permission_classes = (custom_permission.AllowAny,)
    serializer_class = serializers.AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request, *args, **kwargs):

        serializer = serializers.AuthTokenSerializer(
            data=request.data, context={"request": request}
)

        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "date_joined": {
                    "year": user.date_joined.year,
                    "month": user.date_joined.month,
                    "day": user.date_joined.day,
                    "time": user.date_joined.time().strftime("%H:%M:%S"),
                },
                "date_updated": {
                    "year": user.date_updated.year,
                    "month": user.date_updated.month,
                    "day": user.date_updated.day,
                    "time": user.date_updated.time().strftime("%H:%M:%S"),
                },
            }
        )
