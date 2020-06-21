from .models import CODOrder
import django_filters
from django_filters import rest_framework as filters


class CharFilterInFilter(filters.BaseInFilter, filters.CharFilter):
    pass


class OrdersFilter(django_filters.FilterSet):
    Categories = CharFilterInFilter(field_name='Categories__title', lookup_expr='in')
    city = CharFilterInFilter(field_name='city__title', lookup_expr='in')

    class Meta:
        model = CODOrder
        fields = ['Categories', 'city']
