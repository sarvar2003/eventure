from django.db import models
from api.models import choices

class Event(models.Model):
    
    """Event model"""

    host = models.ForeignKey("api.User", related_name='Host', on_delete=models.CASCADE)
    guests = models.ManyToManyField("api.User", related_name='Guests', blank=True, null=True)
    title = models.CharField(max_length=250)
    slug_title = models.SlugField()
    category = models.ForeignKey("api.Category", on_delete=models.SET_NULL, blank=True, null=True)
    topics = models.ManyToManyField("api.Topic", blank=True, null=True)
    language = models.CharField(max_length=50, choices=choices.LANGUAGE_CHOICES)
    location = models.CharField(max_length=250)
    date_time = models.DateTimeField(auto_now=False, auto_now_add=False)
    number_of_seats = models.PositiveIntegerField()
    ticket_price = models.DecimalField(max_digits=6, decimal_places=2)
    currency = models.CharField(max_length=50, choices=choices.CURRENCY_CHOICES)
    thumbnail = models.FileField(upload_to=None, max_length=100)
    description = models.TextField()


    def __str__(self) -> str:
        return self.slug_title
