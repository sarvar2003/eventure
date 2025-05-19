from django.urls import path

from . import views

urlpatterns = [
    path("", views.AllEventsAPIView.as_view(), name="all-events"),
    path("create/", views.CreateEventAPIView.as_view(), name="create-event"),
    path("event/<int:id>/", views.RetrieveEventAPIView.as_view(), name="event-info"),
    path("event/<int:id>/update/", views.UpdateEventAPIView.as_view(), name="update-event"),
    path("user-events/<str:email>/", views.ListUserEventsAPIView.as_view(), name="user-events"),
    path("topics/", views.ListTopicsAPIView.as_view({'get': 'list'}), name="topics"),
]  