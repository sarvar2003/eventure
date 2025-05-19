import datetime
from django.test import TestCase
from django.utils import timezone
from rest_framework.test import APIClient

from events.models import Event, Topic
from users.models import User


class EventModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            email="host@example.com",
            first_name="Host",
            last_name="User",
            password="password123",
        )
        self.future_date = timezone.now() + datetime.timedelta(days=10)
        Topic.objects.create(name="test_topic")
        self.topic = Topic.objects.get(name="test_topic")

    def test_event_creation(self):
        event = Event.objects.create(
            host=self.user,
            title="Tech Conference",
            language="en",
            location="Tashkent",
            date_time=self.future_date,
            number_of_seats=100,
            ticket_price=20.00,
            currency="USD",
            description="A tech event.",
        )
        event.topics.add(self.topic)

        self.assertEqual(event.title, "Tech Conference")
        self.assertEqual(event.slug_title, "tech-conference")
        self.assertIn(self.topic, event.topics.all())
        self.assertEqual(event.language, "en")

    def test_slug_generation(self):
        event = Event.objects.create(
            host=self.user,
            title="My Cool Event",
            language="en",
            location="Tashkent",
            date_time=self.future_date,
            number_of_seats=50,
            ticket_price=15.00,
            currency="USD",
            description="Coolest event ever.",
        )

        self.assertEqual(event.slug_title, "my-cool-event")

    def test_event_past_date_is_allowed_by_model(self):
        past_date = timezone.now() - datetime.timedelta(days=1)
        event = Event.objects.create(
            host=self.user,
            title="Old Event",
            language="en",
            location="Tashkent",
            date_time=past_date,
            number_of_seats=10,
            ticket_price=0,
            currency="USD",
            description="Past event.",
        )
        self.assertEqual(event.date_time.date(), past_date.date())


class EventFilterTest(TestCase):

    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(
            email="filterhost@example.com",
            first_name="Filter",
            last_name="Host",
            password="password123",
        )

        Topic.objects.create(name="test_topic1")
        Topic.objects.create(name="test_topic2")
        self.topic1 = Topic.objects.get(name="test_topic1")
        self.topic2 = Topic.objects.get(name="test_topic2")

        self.event1 = Event.objects.create(
            host=self.user,
            title="Tech Meetup",
            language="en",
            location="Tashkent",
            date_time=timezone.now() + datetime.timedelta(days=5),
            number_of_seats=100,
            ticket_price=10,
            currency="USD",
            description="A tech meetup.",
        )
        self.event1.topics.add(self.topic1)

        self.event2 = Event.objects.create(
            host=self.user,
            title="Tech Summit",
            language="uz",
            location="Tashkent",
            date_time=timezone.now() + datetime.timedelta(days=15),
            number_of_seats=100,
            ticket_price=15,
            currency="USD",
            description="Tech conference.",
        )
        self.event2.topics.add(self.topic2)

    def test_filter_by_language(self):
        response = self.client.get("/events/?language=uz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Tech Summit")

    def test_filter_by_topic(self):
        response = self.client.get(f"/events/?topics={self.topic1.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Tech Meetup")

    def test_filter_by_date_range(self):
        start_date = (timezone.now() + datetime.timedelta(days=1)).date()
        end_date = (timezone.now() + datetime.timedelta(days=10)).date()
        response = self.client.get(
            f"/events/?start_date={start_date}&end_date={end_date}"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Tech Meetup")

    def test_combined_filter(self):
        response = self.client.get(f"/events/?language=uz&topics={self.topic2.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Tech Summit")
