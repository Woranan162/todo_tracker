from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """
    Custom permission to only allow owners of a task to access it.
    """
    message = "You do not have permission to access this task."

    def has_object_permission(self, request, view, obj):
        """
        Check if the requesting user is the owner of the object.
        """
        return obj.user == request.user