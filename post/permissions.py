from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    """
    Разрешение, позволяющее редактировать/удалять объект только автору или администратору.
    """

    def has_object_permission(self, request, view, obj):
        # Чтение разрешено всем
        if request.method in permissions.SAFE_METHODS:
            return True

        # Запись/удаление разрешены только автору или администратору
        return obj.author == request.user or request.user.is_staff