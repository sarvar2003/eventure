from django.db import models
from django.utils.text import slugify

from core import choices


class Event(models.Model):
    """Event model"""

    host = models.ForeignKey(
        "users.User", related_name="Host", on_delete=models.CASCADE
    )
    guests = models.ManyToManyField("users.User", related_name="Guests")
    title = models.CharField(max_length=250)
    slug_title = models.SlugField()
    topics = models.ManyToManyField("Topic", related_name="Topics", blank=True)
    language = models.CharField(
        max_length=50, choices=choices.LANGUAGE_OPTIONS, default="en"
    )
    location = models.CharField(max_length=250)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    number_of_seats = models.PositiveIntegerField()
    ticket_price = models.DecimalField(
        max_digits=6, decimal_places=2, default=0.00, blank=True, null=True
    )
    currency = models.CharField(
        max_length=50,
        choices=choices.CURRENCY_OPTIONS,
        default="USD",
        blank=True,
        null=True,
    )
    thumbnail = models.FileField(
        upload_to="images/", max_length=100, blank=True, null=True
    )
    description = models.TextField()

    def save(self, *args, **kwargs) -> None:
        self.slug_title = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug_title


class Topic(models.Model):
    """Topic model"""

    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
