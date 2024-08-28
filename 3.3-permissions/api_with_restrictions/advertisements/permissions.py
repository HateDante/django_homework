from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAuthenticated


class IsAutorOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or IsAuthenticated() and obj.creator == request.user


class IsAdminUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return bool(request.user and request.user.is_staff)
