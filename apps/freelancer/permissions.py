from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        user = f'{obj.first_name} {obj.last_name} --> {obj.profession}'
        return request.user == user or request.user.is_superuser is True