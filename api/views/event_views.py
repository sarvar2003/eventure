from rest_framework import views, generics

from api.serializers import event_serializers
from api.models import event
from api.permissions import permissions

class AllEventsAPIView(generics.ListAPIView):

    """API view to list all events"""

    serializer_class = event_serializers.EventSerializer
    queryset = event.Event.objects.all()
    permission_classes = (permissions.AllowAny,)


class CreateEventAPIView(generics.CreateAPIView):

    """API view to create event"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)


class RetrieveEventAPIView(generics.RetrieveAPIView):

    """API view to retrieve event"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return event.Event.objects.get(id=self.kwargs.get('id'))


class UpdateEventAPIView(generics.RetrieveUpdateDestroyAPIView):

    """API view to update event"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def get_object(self):
        return event.Event.objects.get(id=self.kwargs.get('id'))


class FilterEventsAPIView(generics.ListAPIView):

    """API view for filtering events"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = event.Event.objects.all()

    def get_queryset(self):

        """Filters according to category, topic and language of events"""

        category_filters = self.kwargs.get('category').lower().split('+')
        topic_filters = self.kwargs.get('topic').lower().split('+')
        language_filters = self.kwargs.get('language').capitalize()

        if category_filters:
            self.queryset = self.queryset.filter(category__slug_title__in=category_filters)
        
        if topic_filters:
            self.queryset = self.queryset.filter(topics__slug_title__in=topic_filters)
        
        if language_filters:
            self.queryset = self.queryset.filter(language=language_filters)

        return self.queryset
