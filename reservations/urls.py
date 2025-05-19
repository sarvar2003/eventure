from django.urls import path

from . import views

urlpatterns = [
    path("", views.ListReservationsAPIView.as_view(), name="all-reservations"),
    path("create/", views.CreateReservationAPIView.as_view(), name="create-reservation"),
    path("event-reservations/<int:event_id>/", views.ListEventReservationsAPIView.as_view(), name='event-reservations'),
    path("user-reservations/<str:email>/", views.ListUserReservationsAPIView.as_view(), name="user-reservation"),
    path("reservation/<int:id>/", views.RetreiveReservation.as_view(), name="retrieve-reservation")
]