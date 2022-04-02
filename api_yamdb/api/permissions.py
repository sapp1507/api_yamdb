from django.contrib.auth import get_user_model
from rest_framework.permissions import SAFE_METHODS, BasePermission

User = get_user_model()


class IsAuthorOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user or request.method in SAFE_METHODS


class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and (
            user.role == User.ADMIN or user.is_superuser
        )


class AdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        return (request.user.is_authenticated
                and (request.user.role == User.ADMIN
                     or request.user.is_superuser)
                or request.method in SAFE_METHODS)


class ReviewCommentPermissions(BasePermission):
    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if view.action == 'retrieve':
            return True
        if view.action in ['partial_update', 'destroy']:
            if (request.user == obj.author
                    or request.user.role == User.ADMIN
                    or request.user.role == User.MODERATOR):
                return True
        return False
