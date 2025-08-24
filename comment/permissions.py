from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """Проверка, что пользователь автор или администратор"""

    class IsAuthorOrAdmin(permissions.BasePermission):
        def has_object_permission(self, request, view, obj):
            if request.method in permissions.SAFE_METHODS:
                return True
            return obj.author == request.user or request.user.is_staff
