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
        return event.Event.objects.filter(slug_title=self.kwargs.get('slug_title')).get(id=self.kwargs.get('id'))


class UpdateEventAPIView(generics.RetrieveUpdateDestroyAPIView):

    """API view to update event"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.IsOwnerOrReadOnly,)

    def get_object(self):
        return event.Event.objects.filter(slug_title=self.kwargs.get('slug_title')).get(id=self.kwargs.get('id'))


class FilterByCategoryAPIView(generics.ListAPIView):

    """API view for filtering events by category"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = event.Event.objects.all()

    def get_queryset(self):

        """Filters according to category of events"""

        category_filters = self.kwargs.get('category').lower().split('+')

        if category_filters:
            self.queryset = self.queryset.filter(category__slug_title__in=category_filters)

        return self.queryset


class FilterByTopicAPIView(generics.ListAPIView):

    """API view for filtering events by topic"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = event.Event.objects.all()

    def get_queryset(self):

        """Filters according to topic of events"""

        topic_filters = self.kwargs.get('topic').lower().split('+')

        if topic_filters:
            self.queryset = self.queryset.filter(topics__slug_title__in=topic_filters)

        print(type(self.queryset))

        return self.queryset


class FilterByLanguageAPIView(generics.ListAPIView):

    """API view for filtering events by language"""

    serializer_class = event_serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = event.Event.objects.all()

    def get_queryset(self):

        """Filters according to language of events"""

        language_filters = self.kwargs.get('language').capitalize().split('+')

        if language_filters:
            self.queryset = self.queryset.filter(language__in=language_filters)

        return self.queryset
