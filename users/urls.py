from django.urls import path

from users import views

urlpatterns = [
    path("all/", views.AllUsersAPIView.as_view(), name="all-users"),
    path("register/", views.UserAPIView.as_view(), name="register"),
    path("user/token/", views.ObtainAuthTokenView.as_view(), name="token"),
    path("verify-email/<str:token>/", views.VerifyEmailAPIView.as_view(), name="verify-email"),
    path("user/<str:email>/", views.RetrieveUserAPIView.as_view(), name="retrieve-user"),
    path("user/update/<str:email>/", views.UpdateUserAPIView.as_view(), name="update-user"),
    path("send-password-reset-link/", views.SendPasswordResetLinkAPIView.as_view(), name="send-password-reset-link"),
    path("reset-password/<str:token>/", views.ResetPasswordAPIView.as_view(), name="reset-password"),
    path("verify-token/", views.VerifyTokenAPIView.as_view(), name="verify-token"),
]
