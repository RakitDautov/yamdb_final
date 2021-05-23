from rest_framework import permissions


class IsAuthorOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.author == request.user or
            request.method in permissions.SAFE_METHODS or
            request.user.is_admin or request.user.is_moderator
        )


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS or \
           (request.user and request.user.is_staff)
