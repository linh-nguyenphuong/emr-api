from rest_framework.permissions import BasePermission

# Application imports
from templates.error_template import ErrorTemplate

class IsAdmin(BasePermission):
    message = ErrorTemplate.ADMIN_REQUIRED

    def has_permission(self, request, view):
        return request.user.role.name == 'admin' and request.user.is_active

class IsUser(BasePermission):
    message = ErrorTemplate.USER_REQUIRED
    user_role = ('receptionist', 'physician', 'patient')

    def has_permission(self, request, view):
        return request.user.role.name in user_role and request.user.is_active