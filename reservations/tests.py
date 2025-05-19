import datetime

from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from events.models import Event
from .models import Reservation
from events.models import Topic

User = get_user_model()


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            email="guest@example.com",
            first_name="Guest",
            last_name="User",
            password="password123",
        )

        self.host = User.objects.create_user(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            password="password123",
        )

        self.future_date = timezone.now() + datetime.timedelta(days=10)

        business_topic, _ = Topic.objects.get_or_create(name="business")

        self.event = Event.objects.create(
            host=self.host,
            title="Big Tech Event",
            language="en",
            location="Tashkent",
            date_time=self.future_date,
            number_of_seats=100,
            ticket_price=50.00,
            currency="USD",
            description="A very big event.",
        )

        self.event.topics.set([business_topic])

    def test_create_reservation_successfully(self):
        reservation = Reservation.objects.create(
            event=self.event, guest=self.user, number_of_tickets=2
        )
        self.assertEqual(reservation.number_of_tickets, 2)
        self.assertEqual(reservation.status, "confirmed")
        self.assertEqual(reservation.total_price, 100.00)

        self.event.refresh_from_db()
        self.assertEqual(self.event.number_of_seats, 98)

    def test_reservation_not_enough_seats(self):
        self.event.number_of_seats = 1
        self.event.save()

        with self.assertRaises(ValidationError):
            Reservation.objects.create(
                event=self.event, guest=self.user, number_of_tickets=2
            )

    def test_reservation_exactly_available_seats(self):
        self.event.number_of_seats = 3
        self.event.save()

        reservation = Reservation.objects.create(
            event=self.event, guest=self.user, number_of_tickets=3
        )
        self.event.refresh_from_db()
        self.assertEqual(self.event.number_of_seats, 0)

    def test_total_price_property(self):
        reservation = Reservation.objects.create(
            event=self.event, guest=self.user, number_of_tickets=5
        )
        expected_price = self.event.ticket_price * 5
        self.assertEqual(reservation.total_price, expected_price)
