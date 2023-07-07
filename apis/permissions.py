from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        """Access to object list"""
        if request.user.is_authenticated:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        """Access to object detail"""
        # Read permissions are allowed to any request, so we'll always
        # allow GET, HEAD, or OPTIONS requests
        if request.method in permissions.SAFE_METHODS:
            return True
        # Write permissions are only allowed to the author of a post
        return obj.user == request.user  # request.user.groups.filter(name=name).exists()
