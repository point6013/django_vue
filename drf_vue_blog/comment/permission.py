from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = "you must be the owner to update"

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_autherticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        return obj.author == request.user
