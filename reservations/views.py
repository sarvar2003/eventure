from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _

from rest_framework.response import Response
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser

from . import serializers
from . import models
from core import custom_permission, utils


class ListReservationsAPIView(generics.ListAPIView):
    """API view to list all reservations"""

    serializer_class = serializers.ReservationSerializer
    permission_classes = (custom_permission.AllowAny,)
    queryset = models.Reservation.objects.all()


class ListEventReservationsAPIView(generics.ListAPIView):
    """API view to list event reservations"""

    serializer_class = serializers.ReservationSerializer
    permission_classes = (custom_permission.AllowAny,)
    queryset = models.Reservation.objects.all()

    def get_queryset(self):
        return self.queryset.filter(event=self.kwargs.get("event_id"))


class ListUserReservationsAPIView(generics.ListAPIView):
    """API view to list user reservations"""

    serializer_class = serializers.ReservationSerializer
    permission_classes = (custom_permission.AllowAny,)
    queryset = models.Reservation.objects.all()

    def get_queryset(self):
        email = self.kwargs.get("email")

        try:
            user = get_user_model().objects.get(email=self.kwargs.get("email"))
            return self.queryset.filter(guest=user)
        except get_user_model().DoesNotExist:
            return self.queryset.none()


class CreateReservationAPIView(generics.CreateAPIView):
    """API view to create reservations"""

    serializer_class = serializers.ReservationSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = (JSONParser,)

    def perform_create(self, serializer):
        reservation = serializer.save(guest=self.request.user)

        event = reservation.event
        event.guests.add(self.request.user)
        event.save()

        self.send_confirmation_email(reservation)

    def send_confirmation_email(self, reservation):
        """Send email after successful reservation creation."""

        pdf_ticket = utils.generate_pdf(reservation)
        if pdf_ticket:
            attachment = pdf_ticket.getvalue()
        else:
            attachment = None

        html_message = render_to_string(
            "reservation_confirmation_email.html",
            context={
                "guest_name": reservation.guest.first_name,
                "event_title": reservation.event.title,
                "event_date": reservation.event.date_time.strftime("%d %B %Y, %H:%M"),
                "location": reservation.event.location,
                "number_of_tickets": reservation.number_of_tickets,
                "total_price": reservation.total_price,
            },
        )

        plain_message = (
            f"Your reservation for '{reservation.event.title}' is confirmed!\n"
            f"Date: {reservation.event.date_time.strftime('%d %B %Y, %H:%M')}\n"
            f"Location: {reservation.event.location}\n"
            f"Number of tickets: {reservation.number_of_tickets}\n"
            f"Total price: ${reservation.total_price}\n\n"
            f"Thank you for choosing Eventure!"
        )

        data = {
            "email_body": plain_message,
            "to_email": reservation.guest.email,
            "email_subject": "Your Reservation Confirmation - Eventure",
            "html_message": html_message,
        }

        if attachment:
            data["attachment"] = {
                "file": attachment,
                "filename": f"ticket_reservation_{reservation.id}.pdf",
                "mimetype": "application/pdf",
            }

        utils.SendEmailUtil.send_mail(data)


class RetreiveReservation(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve a models"""

    serializer_class = serializers.ReservationSerializer
    permission_classes = (custom_permission.IsOwnerOrReadOnly,)
    queryset = models.Reservation.objects.all()

    def get_object(self):
        return self.queryset.get(id=self.kwargs.get("id"))

    def perform_destroy(self, instance):
        event = instance.event
        event.number_of_seats += instance.number_of_tickets
        event.save()

        instance.delete()
