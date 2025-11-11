from rest_framework import permissions

class BlogRolePermission(permissions.BasePermission):
    """
    Custom role-based permissions:
    - Admin: full access
    - Author: can create + edit own posts
    - Reader: read-only
    """

    def has_permission(self, request, view):
        # Everyone logged in can list or retrieve
        if request.method in permissions.SAFE_METHODS:
            return True

        # Only authenticated users for write ops
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        role = getattr(request.user.profile, "role", "reader")

        # Readers: read-only
        if role == "reader":
            return request.method in permissions.SAFE_METHODS

        # Authors: can edit only their own posts
        if role == "author":
            if request.method in ["PUT", "PATCH", "DELETE"]:
                return obj.author == request.user  # requires author field
            return True

        # Admin: full access
        if role == "admin":
            return True

        return False
