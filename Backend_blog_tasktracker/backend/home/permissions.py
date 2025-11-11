from rest_framework.permissions import BasePermission

class IsAuthenticatedUser(BasePermission):
    
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

class IsEmployee(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'employee'

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
