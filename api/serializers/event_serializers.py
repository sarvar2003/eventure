from rest_framework import serializers

from api.models import event

class EventSerializer(serializers.ModelSerializer):

    """Serializer class for Event model"""
    
    formatted_date = serializers.SerializerMethodField()

    class Meta:
        model = event.Event
        fields = ('id', 'host', 'title', 'slug_title', 'category', 'topics', 'language', 'location', 'formatted_date', 'date_created', 'date_updated', 'number_of_seats', 'ticket_price', 'currency', 'thumbnail', 'description')
        prepopulated_fields = ('slug_title',)
        extra_kwargs = {
            'slug_title': {'read_only': True},
            'date_created': {'read_only': True},
            'date_updated': {'read_only': True},
        }

    def get_formatted_date(self, obj):
        
        formatted_date = {
           "year": obj.date_time.year,
            "month": obj.date_time.month,
            "day": obj.date_time.day,
            "time": obj.date_time.time().strftime("%H:%M:%S"),
            "weekday": obj.date_time.strftime('%A')
        }
        
        return formatted_date