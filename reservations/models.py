from django.db import models
from django.core.exceptions import ValidationError

from core import choices


class Reservation(models.Model):
    """Reservation model"""

    event = models.ForeignKey("events.Event", on_delete=models.CASCADE)
    guest = models.ForeignKey("users.User", on_delete=models.CASCADE)
    number_of_tickets = models.PositiveIntegerField()
    status = models.CharField(
        max_length=50, choices=choices.STATUS_OPTIONS, default="confirmed"
    )

    @property
    def total_price(self):
        return self.event.ticket_price * self.number_of_tickets

    def save(self, *args, **kwargs):
        if not self.pk:
            if self.event.number_of_seats <= 0:
                raise ValidationError("No seats available for this event.")

            if self.number_of_tickets > self.event.number_of_seats:
                raise ValidationError(
                    "Not enough seats available for this reservation."
                )
            self.event.number_of_seats -= self.number_of_tickets
            self.event.save()

        super(Reservation, self).save(*args, **kwargs)
