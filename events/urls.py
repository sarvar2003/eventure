from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

topics_router = DefaultRouter()
topics_router.register(r"topics", views.TopicsViewSet, basename="topics")


urlpatterns = [
    path("", views.AllEventsAPIView.as_view(), name="all-events"),
    path("create/", views.CreateEventAPIView.as_view(), name="create-event"),
    path("event/<int:id>/", views.RetrieveEventAPIView.as_view(), name="event-info"),
    path("event/<int:id>/update/",views.UpdateEventAPIView.as_view(),name="update-event"),
    path("user-events/<str:email>/",views.ListUserEventsAPIView.as_view(), name="user-events"),
]

urlpatterns += topics_router.urls