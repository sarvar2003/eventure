from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from rest_framework import views, status
from rest_framework.authtoken.models import Token
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework import generics
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from users import serializers
from users import user_permissions
from users import utils

# Create your views here.


class AllUsersAPIView(generics.ListAPIView):

    """API view for listing users"""

    serializer_class = serializers.UserSerializer
    permission_classes = (user_permissions.AllowAny,)
    queryset = get_user_model().objects.all()


class UserAPIView(views.APIView):

    """API view for User model"""

    serializer_class = serializers.UserSerializer
    permission_classes = (user_permissions.AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        serializer.save()

        user_data = serializer.data

        user = get_user_model().objects.get(email=user_data.get('email'))

        
        token, created_at = Token.objects.get_or_create(user=user)
        current_site_domain = get_current_site(request=request).domain
        relative_url = reverse('verify-email', kwargs={'token': str(token)})    
        absolute_url = 'http://' + current_site_domain + relative_url
        email_body = 'Please use this link below to verify your email for Eventure \n' + absolute_url

        html_message = render_to_string('users/verification-email.html', context={'first_name': user_data.get('first_name'), 'absolute_url': absolute_url})

        data = {'subject': 'Email Verification Eventure', 'body': email_body, 'to': user_data.get('email'), 'html_message': html_message}

        utils.Mail.send_mail(data=data)

        return Response(_('Verification email sent, please check your inbox'), status=status.HTTP_200_OK)


class VerifyEmailAPIView(views.APIView):

    """API view for verifying user email"""

    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (user_permissions.AllowAny,)

    def get(self, request, token):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():

            try:
                user_token = Token.objects.get(key=token)

                user = get_user_model().objects.get(id=user_token.user.id)

                user.is_active = True
                user.is_verified = True
                user.save()

                return Response({
                    'status': _('Email successfully verified'),
                    'user': {
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'is_verified': user.is_verified 
                    }
                }, status=status.HTTP_200_OK)

            except Token.DoesNotExist:
                return Response({'status': _('Invalid Token')}, status=status.HTTP_400_BAD_REQUEST)


class RetrieveUserAPIView(generics.RetrieveAPIView):

    """API view for retrieving user details"""

    serializer_class = serializers.UserSerializer
    permission_classes = (user_permissions.IsOwner, user_permissions.IsOwnerOrReadOnly)

    def get_object(self):
        return get_user_model().objects.get(email=self.kwargs.get('email'))


class UpdateUserAPIView(generics.RetrieveUpdateDestroyAPIView):

    """API view for updating user details"""

    serializer_class = serializers.UpdateUserSerializer
    permission_classes = (user_permissions.IsOwnerOrReadOnly,)

    def get_object(self):
        return get_user_model().objects.get(email=self.kwargs.get('email'))


class SendPasswordResetLinkAPIView(views.APIView):

    """API view for sending password reset link"""

    serializer_class = serializers.SendResetLinkSerializer
    permission_classes = (user_permissions.AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=False)

        try:
            user = get_user_model().objects.get(email=serializer.data.get('email'))

            token, created_at = Token.objects.get_or_create(user=user)
            current_site_domain = get_current_site(request=request).domain 
            relative_url = reverse('reset-password', kwargs={'token': token})
            absolute_url = 'http://' + current_site_domain + relative_url
            email_body = f'Hello, {user.first_name}, use the link below to reset your password \n\n {absolute_url}' 
            html_message = render_to_string('users/password-reset-link-email.html', context={'first_name': user.first_name, 'absolute_url': absolute_url})

            data = {'subject': 'Eventure Password Reset', 'body': email_body, 'to': user.email, 'html_message': html_message}

            utils.Mail.send_mail(data=data)

            return Response(_('Password reset link has been successfully sent, please check your inbox'), status=status.HTTP_200_OK)

        except get_user_model().DoesNotExist:
            return Response(_('User with the given email does not exist in our system. Please, make sure to enter your email that is linked to your Eventure account'), status=status.HTTP_400_BAD_REQUEST)


class ResetPasswordAPIView(views.APIView):

    """API view for user password reset"""

    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (user_permissions.AllowAny,)

    def get(self, request, token):
        
        try:
            user_token = Token.objects.get(key=token)

            try:
                get_user_model().objects.get(id=user_token.user.id)

                return Response({'status': 'valid'}, status=status.HTTP_200_OK)

            except get_user_model().DoesNotExist:
                return Response({'status': 'User does not exist in our system, please contact customer support'}, status=status.HTTP_400_BAD_REQUEST)
    
        except Token.DoesNotExist:
            return Response({'status': 'Invalid Token'}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, token):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        user_token, created_at = Token.objects.get(key=token)
        
        user = get_user_model().objects.get(id=user_token.user.id)

        new_password = serializer.validated_data['confirm_password']

        user.set_password(new_password)

        user.save()

        return Response(_('Password has been successfully reset'), status=status.HTTP_200_OK)
     

class VerifyTokenAPIView(views.APIView):

    """API view for verifying token"""

    serializer_class = serializers.VerifyTokenSerializer
    permission_classes = (user_permissions.AllowAny,)

    def post(self, request):

        serializer = self.serializer_class(data=request.data)
        
        serializer.is_valid(raise_exception=True)

        token = serializer.data.get('token')

        try:
            user_token = Token.objects.get(key=token)

            try:
                user = get_user_model().objects.get(id=user_token.user.id)

                return Response({
                    'status': 'valid',
                    'token': str(token),
                    'user': {
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        "date_joined": {
                            "year": user.date_joined.year,
                            "month": user.date_joined.month,
                            "day": user.date_joined.day,
                            "time": user.date_joined.time().strftime("%H:%M:%S"),
                        },
                        "date_updated": {
                            "year": user.date_joined.year,
                            "month": user.date_joined.month,
                            "day": user.date_joined.day,
                            "time": user.date_joined.time().strftime("%H:%M:%S"),
                        },       
                    }

                }, status=status.HTTP_200_OK)

            except get_user_model().DoesNotExist:
                return Response({'status': 'User does not exist in our system, please contact customer support'}, status=status.HTTP_400_BAD_REQUEST)

        except Token.DoesNotExist:
            return Response({'status' : _('Invalid Token')} , status=status.HTTP_400_BAD_REQUEST)


class ObtainAuthTokenView(ObtainAuthToken):

    """API view for obtaining auth token"""

    serializer_class = serializers.AuthTokenSerializer
    permission_classes = (user_permissions.AllowAny,)
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    def post(self, request):
        
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data.get('user')

        token, created_at = Token.objects.get_or_create(user=user)

        return Response({
                "token": str(token),
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
                    "year": user.date_joined.year,
                    "month": user.date_joined.month,
                    "day": user.date_joined.day,
                    "time": user.date_joined.time().strftime("%H:%M:%S"),
                },
            }, status=status.HTTP_200_OK)

