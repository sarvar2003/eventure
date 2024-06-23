from django.urls import path

from api.views import user_views

urlpatterns = [
    path("all/", user_views.AllUsersAPIView.as_view(), name="all-users"),
    path("register/", user_views.UserAPIView.as_view(), name="register"),
    path("user/token/", user_views.ObtainAuthTokenView.as_view(), name="token"),
    path("verify-email/<str:token>/", user_views.VerifyEmailAPIView.as_view(), name="verify-email"),
    path("user/<str:email>/", user_views.RetrieveUserAPIView.as_view(), name="retrieve-user"),
    path("user/update/<str:email>/", user_views.UpdateUserAPIView.as_view(), name="update-user"),
    path("send-password-reset-link/", user_views.SendPasswordResetLinkAPIView.as_view(), name="send-password-reset-link"),
    path("reset-password/<str:token>/", user_views.ResetPasswordAPIView.as_view(), name="reset-password"),
    path("verify-token/", user_views.VerifyTokenAPIView.as_view(), name="verify-token"),
]
