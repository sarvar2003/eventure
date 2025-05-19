from rest_framework import serializers

from . import models



class ReservationSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source='event.title', read_only=True)
    event_location = serializers.CharField(source='event.location', read_only=True)
    event_date_time = serializers.DateTimeField(source='event.date_time', read_only=True)
    
    class Meta:
        model = models.Reservation
        fields = ['id', 'event', 'event_title', 'event_location', 'event_date_time', 'number_of_tickets']
        read_only_fields = ['guest',]


    
    
# class ReservationSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = models.Reservation
#         fields = ['event', 'number_of_tickets']
#         read_only_fields = ['guest']
