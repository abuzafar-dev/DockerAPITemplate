from rest_framework import permissions


class UserPermission(permissions.BasePermission):
    """Ro'yxatdan o'tish hammaga ochiq; qolgani — faqat o'zi yoki admin."""

    def has_permission(self, request, view):
        if view.action == 'create':
            return True
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
