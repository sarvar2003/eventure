from rest_framework import serializers
from django.utils import timezone
from users.serializers import UserSerializer

from . import models



class TopicSerializer(serializers.ModelSerializer):
    """Serializer class for Topic model"""

    class Meta:
        model = models.Topic
        fields = '__all__'



class EventSerializer(serializers.ModelSerializer):
    """Serializer class for Event model"""

    host_name = serializers.CharField(source='host.get_full_name', read_only=True)
    guests = UserSerializer(many=True, read_only=True)
    formatted_date = serializers.SerializerMethodField()
    topics = TopicSerializer(many=True, read_only=True) 
    topic_ids = serializers.PrimaryKeyRelatedField(
        queryset=models.Topic.objects.all(),
        many=True,
        write_only=True,
        source="topics" 
    )

    class Meta:
        model = models.Event
        fields = (
            "id",
            "host",
            "guests",
            "title",
            "slug_title",
            "topics",
            "topic_ids", 
            "language",
            "location",
            "date_time",
            "formatted_date",
            "date_created",
            "date_updated",
            "number_of_seats",
            "thumbnail",
            "description",
            "host_name",
        )
        prepopulated_fields = ("slug_title",)
        extra_kwargs = {
            "slug_title": {"read_only": True},
            "date_created": {"read_only": True},
            "date_updated": {"read_only": True},
        }
        read_only_fields = ("slug_title", "date_created", "date_updated", "host_name", "host", "topics", "guests")
        
    def validate_date_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Event date/time cannot be in the past.")
        return value

    def get_formatted_date(self, obj):

        formatted_date = {
            "year": obj.date_time.year,
            "month": obj.date_time.month,
            "day": obj.date_time.day,
            "time": obj.date_time.time().strftime("%H:%M:%S"),
            "weekday": obj.date_time.strftime("%A"),
        }
        return formatted_date
    