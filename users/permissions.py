from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            if request.method in SAFE_METHODS and request.user.is_admin:
                return True
            else:
                return (
                    request.user and request.user.is_staff
                ) or request.user.is_admin
