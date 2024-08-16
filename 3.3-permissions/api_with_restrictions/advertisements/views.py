from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement, AdvertisementFilter
from advertisements.permissions import IsAutorOrReadOnly, IsAdminUser
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = AdvertisementFilter

    def list(self, request, *args, **kwargs):
        get_data = super().list(request, *args, **kwargs).data
        user = self.request.user.id
        new_data = [res for res in get_data if user == res['creator']['id'] or res['status'] != 'DRAFT']
        return Response(new_data)

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.user.is_staff:
            return [IsAdminUser()]
        return [IsAutorOrReadOnly()]
