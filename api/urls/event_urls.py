from django.urls import path

from api.views import event_views

urlpatterns = [
    path("all/", event_views.AllEventsAPIView.as_view(), name="all-events"),
    path("create/", event_views.CreateEventAPIView.as_view(), name="create-event"),
    path("event/<slug:slug_title>/<int:id>/", event_views.RetrieveEventAPIView.as_view(), name="event-info"),
    path("event/update/<str:slug_title>/<int:id>/", event_views.UpdateEventAPIView.as_view(), name="update-event"),
    path("filter/category/<str:category>/", event_views.FilterByCategoryAPIView.as_view(), name='category-filter'),
    path("filter/topic/<str:topic>/", event_views.FilterByTopicAPIView.as_view(), name='topic-filter'),
    path("filter/language/<str:language>/", event_views.FilterByLanguageAPIView.as_view(), name='language-filter'),
]
