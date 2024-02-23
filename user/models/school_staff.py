from django.db import models
from . import Role
from . import SchoolStaffManager
from . import User
from schools.models import School


class SchoolStaffProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="school_staff")
    school = models.ForeignKey(School,on_delete=models.SET_NULL,null=True,related_name='school_staff')


class SchoolStaff(User):
    base_role = Role.SCHOOL_STAFF
    school_staffs = SchoolStaffManager()
    
    class Meta:
        proxy = True

    def __str__(self):
        return f'{self.username} - {self.role}'
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        SchoolStaffProfile.objects.update_or_create(user=self)
    