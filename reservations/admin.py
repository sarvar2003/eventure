from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('event', 'guest', 'number_of_tickets', 'status', 'total_price_display')
    search_fields = ('event__title', 'guest__email')
    list_filter = ('status',)
    ordering = ('-id',)

    def total_price_display(self, obj):
        return f"{obj.total_price} {obj.event.currency}"
    total_price_display.short_description = 'Total Price'
