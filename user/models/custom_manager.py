from django.contrib.auth.base_user import BaseUserManager
from . import Role


class SchoolStaffManager(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=Role.SCHOOL_STAFF)