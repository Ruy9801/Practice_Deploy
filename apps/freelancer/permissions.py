from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
<<<<<<< HEAD
        return request.user == obj.owner or request.user.is_superuser is True
=======
        user = f'{obj.first_name} {obj.last_name} --> {obj.profession}'
        return request.user == user or request.user.is_superuser is True
>>>>>>> 1197d5402ca665d1214941dd2aa1f8309592546e
