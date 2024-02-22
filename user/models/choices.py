from django.db import models

class Role(models.TextChoices):
    ADMIN = "ADMIN",'Admin'
    SCHOOL_STAFF = "SCHOOL_STAFF","SchoolStaff"
    STUDENT = "STUDENT","Student"
    DRIVER = "DRIVER","Driver"


class Gender(models.TextChoices):
    Male = "Male",'Male'
    Female = "Female",'Female'