from django_filters.rest_framework import DjangoFilterBackend

from django.shortcuts import get_object_or_404

from rest_framework import generics, viewsets, status
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.response import Response

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
        if thumbnail:
            serializer.instance.thumbnail = thumbnail
            serializer.instance.save()

        topics = self.request.data.get("topics")
        print(self.request.data)
        if topics:
            topic_list = []
            for id in topics:
                topic_obj = get_object_or_404(Topic, id=id)
                topic_list.append(topic_obj)
                print(topic_obj)
            serializer.instance.topics.set(topic_list)
            serializer.instance.save()
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

    def post(self, serializer, *args, **kwargs):
        id = kwargs.get("id")
        if id:
            event = Event.objects.get(id=id)
            serializer = self.serializer_class(event, data=self.request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            
            thumbnail = self.request.data.get("thumbnail")
            if thumbnail:
                serializer.instance.thumbnail = thumbnail
                serializer.instance.save()

            topics = self.request.data.get("topics")
            if topics:
                topic_list = []
                for id in topics:
                    topic_obj = get_object_or_404(Topic, id=id)
                    topic_list.append(topic_obj)
                serializer.instance.topics.set(topic_list)
            else:
                serializer.instance.topics.set([])
            return Response(serializer.data, status=status.HTTP_200_OK)
            

        


class ListTopicsAPIView(viewsets.ReadOnlyModelViewSet):
    """API view to list topics"""

    serializer_class = serializers.TopicSerializer
    permission_classes = (permissions.AllowAny,)
    queryset = Topic.objects.all()

class RetrieveTopicAPIView(generics.RetrieveAPIView):
    """API view to retrieve topic"""

    serializer_class = serializers.TopicSerializer
    permission_classes = (permissions.AllowAny,)

    def get_object(self):
        return Topic.objects.get(id=self.kwargs.get("id"))
