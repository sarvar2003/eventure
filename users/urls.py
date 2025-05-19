from django.urls import path

from users import views


app_name = 'users'


urlpatterns = [
    path('', views.AllUsers.as_view(), name='all-users'),
    path('create/', views.UserAPIView.as_view(), name='create-user'),
    path('me/', views.CurrentUserAPIView.as_view(), name='current-user'),
    path('me/update/<str:email>/', views.UpdateUserAPIView.as_view(), name='update-user'),
    path('send_password_reset_link/', views.SendPasswordResetEmailAPIView.as_view(), name='send-password-reset-link'),
    path('password_reset/<str:token>/', views.PasswordResetAPIView.as_view(), name='password-reset'),
    path('token/', views.AuthTokenAPIView.as_view(), name='user-token'),
    path('verify_email/<str:token>/', views.VerifyEmail.as_view(), name='email-verify'),
    path("send_email_verification/", views.SendVerificationEmail.as_view(), name="send-email-verification"),
    path('verify_token/', views.VerifyToken.as_view(), name='token-verification'),
]