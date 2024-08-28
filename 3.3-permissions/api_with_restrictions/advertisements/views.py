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

    def list(self, request, *args, **kwargs):
        # Объявления со статусом 'DRAFT' должны быть доступны только для автора
        queryset = self.get_queryset().filter(~Q(status='DRAFT') | Q(creator=self.request.user.id))
        serializer = AdvertisementSerializer(queryset, many=True)
        return Response(serializer.data)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user.is_staff:
            return [IsAdminUser()]
        return [IsAutorOrReadOnly()]
