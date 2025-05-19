from rest_framework.permissions import BasePermission, SAFE_METHODS


class AllowAny(BasePermission):
    """Permission to Allow anyone"""

    def has_object_permission(self, request, view, obj):
        return True


class IsOwnerOrReadOnly(BasePermission):
    """Permission to Allow Owners of the current object or the users with read only access."""

    def has_object_permission(self, request, view, obj):

        if request.method in SAFE_METHODS:
            return True

        return obj.id == request.user.id or request.user.is_staff


class IsOwner(BasePermission):
    """Permission to Allow if the object belongs to the current user."""

    def has_object_permission(self, request, view, obj):
        return obj.id == request.user.id


class IsAdmin(BasePermission):
    """Permission to Allow if the current user is admin"""

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff
