from django.urls import path

from api.views import event_views

urlpatterns = [
    path("all/", event_views.AllEventsAPIView.as_view(), name="all-events"),
    path("create/", event_views.CreateEventAPIView.as_view(), name="create-event"),
    path("event/<int:id>/", event_views.RetrieveEventAPIView.as_view(), name="event-info"),
    path("event/update/<int:id>/", event_views.UpdateEventAPIView.as_view(), name="update-event"),
    path("filter/<str:category>/<str:topic>/<str:language>/", event_views.FilterEventsAPIView.as_view(), name='filter-events'),
]
