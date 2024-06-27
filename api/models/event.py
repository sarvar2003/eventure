from django.db import models
from django.utils.text import slugify

from typing import Iterable
from api.models import choices

class Event(models.Model):
    
    """Event model"""

    host = models.ForeignKey("api.User", related_name='Host', on_delete=models.CASCADE)
    guests = models.ManyToManyField("api.User", related_name='Guests')
    title = models.CharField(max_length=250)
    slug_title = models.SlugField()
    category = models.ForeignKey("api.Category", on_delete=models.SET_NULL, blank=True, null=True)
    topics = models.ManyToManyField("api.Topic")
    language = models.CharField(max_length=50, choices=choices.LANGUAGE_OPTIONS)
    location = models.CharField(max_length=250)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    number_of_seats = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=50, choices=choices.CURRENCY_OPTIONS)
    thumbnail = models.FileField(upload_to='images/', max_length=100, blank=True, null=True)
    description = models.TextField()


    def save(self,*args, **kwargs) -> None:
        self.slug_title = slugify(self.title)
        super(Event, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug_title
