from django.db import models

from api.models import choices

class Reservation(models.Model):

    """Reservation model"""

    event = models.ForeignKey("api.Event", on_delete=models.CASCADE)
    guest = models.ForeignKey("api.User", on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField()
    status = models.CharField(max_length=50, choices=choices.STATUS_OPTIONS, default='pending')


    @property
    def total_price(self):
        return self.event.ticket_price * self.number_of_tickets

