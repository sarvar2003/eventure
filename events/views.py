from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import generics
from rest_framework import viewsets
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser

from . import serializers
from .models import *
from core import custom_permission as permissions
from .filters import EventFilter


class AllEventsAPIView(generics.ListAPIView):
    """API view to list all events"""

    serializer_class = serializers.EventSerializer
    queryset = Event.objects.all()
    permission_classes = (permissions.AllowAny,)
    filter_backends = [
        DjangoFilterBackend,
    ]
    filterset_class = EventFilter


class ListUserEventsAPIView(generics.ListAPIView):
    """API view to list user events"""

    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Event.objects.all()

    def get_queryset(self):
        email = self.kwargs.get("email")
        return self.queryset.filter(host__email=email)


class CreateEventAPIView(generics.CreateAPIView):
    """API view to create event"""

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)

    def perform_create(self, serializer):
        serializer.save(host=self.request.user)
        thumbnail = self.request.data.get("thumbnail")
        print(self.request.data)
        if thumbnail:
            serializer.instance.thumbnail = thumbnail
            serializer.instance.save()

        topics = self.request.data.get("topics")
        if topics:
            topic_list = []
            for id in topics:
                topic_obj = Topic.objects.get(id=id)
                topic_list.append(topic_obj)
            serializer.instance.topics.set(topic_list)
        else:
            serializer.instance.topics.set([])
        return super().perform_create(serializer)


class RetrieveEventAPIView(generics.RetrieveAPIView):
    """API view to retrieve event"""

    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return Event.objects.get(id=self.kwargs.get("id"))


class UpdateEventAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to update event"""

    parser_classes = (JSONParser, FormParser, MultiPartParser)
    serializer_class = serializers.EventSerializer
    permission_classes = (permissions.IsOwner,)

    def get_object(self):
        return Event.objects.get(id=self.kwargs.get("id"))


class ListTopicsAPIView(viewsets.ReadOnlyModelViewSet):
    """API view to list topics"""

    serializer_class = serializers.TopicSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Topic.objects.all()
