import django_filters
from .models import Message
from django.utils import timezone
from datetime import timedelta

class MessageFilter(django_filters.FilterSet):
    conversation = django_filters.UUIDFilter(field_name='conversation__conversation_id')
    sender = django_filters.UUIDFilter(field_name='sender__user_id')
    sent_after = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='gte')
    sent_before = django_filters.DateTimeFilter(field_name='sent_at', lookup_expr='lte')
    last_24h = django_filters.BooleanFilter(method='filter_last_24h')
    last_week = django_filters.BooleanFilter(method='filter_last_week')
    last_month = django_filters.BooleanFilter(method='filter_last_month')

    class Meta:
        model = Message
        fields = ['conversation', 'sender', 'sent_after', 'sent_before', 
                 'last_24h', 'last_week', 'last_month']

    def filter_last_24h(self, queryset, name, value):
        if value:
            return queryset.filter(
                sent_at__gte=timezone.now() - timedelta(days=1)
            )
        return queryset

    def filter_last_week(self, queryset, name, value):
        if value:
            return queryset.filter(
                sent_at__gte=timezone.now() - timedelta(days=7)
            )
        return queryset

    def filter_last_month(self, queryset, name, value):
        if value:
            return queryset.filter(
                sent_at__gte=timezone.now() - timedelta(days=30)
            )
        return queryset 