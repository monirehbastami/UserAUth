from rest_framework import permissions

class IsConfirm(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_email_confirmed:
            return True
        else:
            return False
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_email_confirmed:
            return True
        else:
            return False