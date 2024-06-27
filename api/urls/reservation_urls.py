from django.urls import path

from api.views import reservation_views

urlpatterns = [
    path("all/", reservation_views.ListReservationsAPIView.as_view(), name="all-reservations"),
    path("create/", reservation_views.CreateReservationAPIView.as_view(), name="create-reservation"),
    path("event-reservations/<int:event_id>/", reservation_views.ListEventReservationsAPIView.as_view(), name='event-reservations'),
    path("user-reservations/<str:email>/", reservation_views.ListUserReservationsAPIView.as_view(), name="user-reservation"),
    path("reservation/<int:id>/", reservation_views.RetreiveReservation.as_view(), name="retrieve-reservation")
]
