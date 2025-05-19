from django.contrib import admin
from .models import *
from .forms import EventForm

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    forms = EventForm
    prepopulated_fields = {'slug_title': ('title',)}
    list_display = ('title', 'location', 'date_time', 'number_of_seats', 'ticket_price')
    search_fields = ('title', 'location')
    list_filter = ('language', 'topics', 'currency')
    ordering = ('-date_time',)

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('-name',)