from django.db.models import Q
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.filters import AdvertisementFilter
from advertisements.permissions import IsAutorOrReadOnly, IsAdminUser
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AdvertisementFilter
    lookup_fields = ['status', ]

    def get_queryset(self):
        return self.queryset.filter(~Q(status='DRAFT') | Q(creator=self.request.user.id))

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user.is_staff:
            return [IsAdminUser()]
        return [IsAutorOrReadOnly()]
