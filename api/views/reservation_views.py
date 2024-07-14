from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _

from rest_framework import generics
from rest_framework.response import Response

from api.serializers import reservation_serializer
from api.models import reservation
from api.permissions import permissions

class ListReservationsAPIView(generics.ListAPIView):

    """API view to list all reservations"""

    serializer_class = reservation_serializer.ReservationSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = reservation.Reservation.objects.all() 


class ListEventReservationsAPIView(generics.ListAPIView):

    """API view to list event reservations"""

    serializer_class = reservation_serializer.ReservationSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = reservation.Reservation.objects.all()

    def get_queryset(self):
        return self.queryset.filter(event=self.kwargs.get('event_id'))
    

class ListUserReservationsAPIView(generics.ListAPIView):

    """API view to list user reservations"""

    serializer_class = reservation_serializer.ReservationSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = reservation.Reservation.objects.all()

    def get_queryset(self):
        email = self.kwargs.get('email')

        try:
            user = get_user_model().objects.get(email=self.kwargs.get('email'))
            return self.queryset.filter(guest=user)
        except get_user_model().DoesNotExist:
            return self.queryset.none()

class CreateReservationAPIView(generics.CreateAPIView):

    """API view to create reservations"""

    serializer_class = reservation_serializer.ReservationSerializer
    permission_classes = (permissions.AllowAny,)


class RetreiveReservation(generics.RetrieveUpdateDestroyAPIView):

    """API view to retrieve a reservation"""

    serializer_class = reservation_serializer.ReservationSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)
    queryset = reservation.Reservation.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs.get('id'))

