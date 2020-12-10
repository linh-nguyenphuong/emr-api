from rest_framework.permissions import BasePermission

# Application imports
from templates.error_template import ErrorTemplate

class IsAdmin(BasePermission):
    message = ErrorTemplate.ADMIN_REQUIRED

    def has_permission(self, request, view):
        try:
            return request.user.role.name == 'admin' and request.user.is_active
        except:
            return False

class IsUser(BasePermission):
    message = ErrorTemplate.USER_REQUIRED

    def has_permission(self, request, view):
        try:
            user_role = ('receptionist', 'physician', 'patient')
            return request.user.role.name in user_role and request.user.is_active
        except:
            return False

class IsPhysician(BasePermission):
    message = ErrorTemplate.PHYSICIAN_REQUIRED

    def has_permission(self, request, view):
        try:
            return request.user.role.name == 'physician' and request.user.is_active
        except:
            return False

class IsAdminOrPhysician(BasePermission):
    message = ErrorTemplate.ADMIN_OR_PHYSICIAN_REQUIRED

    def has_permission(self, request, view):
        try:
            user_role = ('admin', 'physician')
            return request.user.role.name in user_role and request.user.is_active
        except:
            return False

class IsPhysicianOrReceptionist(BasePermission):
    message = ErrorTemplate.PHYSICIAN_OR_RECEPTION_REQUIRED

    def has_permission(self, request, view):
        try:
            user_role = ('admin', 'receptionist', 'physician')
            return request.user.role.name in user_role and request.user.is_active
        except:
            return False

class IsPatient(BasePermission):
    message = ErrorTemplate.PHYSICIAN_REQUIRED

    def has_permission(self, request, view):
        try:
            return request.user.role.name == 'patient' and request.user.is_active
        except:
            return False