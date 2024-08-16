from django.conf import settings
from django.db import models
from django_filters import DateFromToRangeFilter, CharFilter
from django_filters.rest_framework import FilterSet


class AdvertisementStatusChoices(models.TextChoices):
    """Статусы объявления."""

    OPEN = "OPEN", "Открыто"
    CLOSED = "CLOSED", "Закрыто"
    DRAFT = "DRAFT", "Черновик"


class Advertisement(models.Model):
    """Объявление."""

    title = models.TextField()
    description = models.TextField(default='')
    status = models.TextField(
        choices=AdvertisementStatusChoices.choices,
        default=AdvertisementStatusChoices.OPEN
    )
    favorites = models.BooleanField(default=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )


class AdvertisementFilter(FilterSet):
    created_at = DateFromToRangeFilter()
    creator = CharFilter(field_name='creator__id')

    class Meta:
        model = Advertisement
        fields = ('created_at', 'favorites', 'creator')
