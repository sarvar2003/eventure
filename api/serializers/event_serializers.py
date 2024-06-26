from rest_framework import serializers

from api.models import event

class EventSerializer(serializers.ModelSerializer):

    """Serializer class for Event model"""

    
    class Meta:
        model = event.Event
        fields = ('id', 'host', 'title', 'slug_title', 'category', 'topics', 'language', 'location', 'date_time', 'date_created', 'date_updated', 'number_of_seats', 'ticket_price', 'currency', 'thumbnail', 'description')
        prepopulated_fields = ('slug_title',)
        extra_kwargs = {
            'slug_title': {'read_only': True},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
        }
