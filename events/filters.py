import django_filters
from .models import *
from django_filters import rest_framework as filters


class EventFilter(django_filters.FilterSet):
    """Filter class for Event model"""

    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    start_date = django_filters.DateTimeFilter(
        field_name="date_time", lookup_expr="gte"
    )
    end_date = django_filters.DateTimeFilter(field_name="date_time", lookup_expr="lte")
    topics = filters.ModelMultipleChoiceFilter(
        field_name="topics", queryset=Topic.objects.all()
    )

    class Meta:
        model = Event
        fields = ["title", "topics", "language"]
