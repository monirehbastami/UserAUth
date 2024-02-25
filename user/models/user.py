from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from .choices import Role,Gender
from uuid import uuid4



class User(AbstractUser, PermissionsMixin):
    profile_picture = models.FileField(max_length=50)
    phone_number = models.CharField(max_length=11)
    national_code = models.CharField(max_length=10,null=False)
    birth_date = models.DateField(null=True)
    gender = models.CharField(max_length=50,choices=Gender.choices)
    role = models.CharField(max_length=50,choices=Role.choices)
    is_email_confirmed = models.BooleanField(default=False)
    base_role = Role.ADMIN

    def __str__(self):
        return f'{self.username} - {self.role}'
    
    def save(self,*args,**kwargs):
        if not self.pk:
            self.role = self.base_role
        return super().save(*args,**kwargs)
    

class EmailConfirmationToken(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete=models.CASCADE)