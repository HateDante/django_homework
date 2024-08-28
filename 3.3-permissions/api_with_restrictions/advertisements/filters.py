from django_filters import rest_framework as filters, DateFromToRangeFilter, CharFilter

from advertisements.models import Advertisement


class AdvertisementFilter(filters.FilterSet):
    """Фильтры для объявлений."""

    created_at = DateFromToRangeFilter()
    creator = CharFilter(field_name='creator__id')

    class Meta:
        model = Advertisement
        fields = ('created_at', 'status', 'creator')
