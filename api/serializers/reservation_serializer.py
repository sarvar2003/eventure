from rest_framework import serializers

from api.models import reservation


class ReservationSerializer(serializers.ModelSerializer):

    """Serializer for reservation model"""

    class Meta:
        model = reservation.Reservation
        fields = ('event', 'guest', 'number_of_tickets', 'status')
        extra_kwargs = {
            'status': {'read_only': True},
        }
