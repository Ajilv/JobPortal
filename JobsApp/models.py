from django.db import models
from django.contrib.auth.models import AbstractUser,AbstractBaseUser
# Create your models here.

class User(AbstractUser):

    class Types(models.TextChoices):
        Emp = "Employee", "Employee"
        Seeker = "Seeker", "Seeker"

    username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
    email = models.EmailField(unique = True)
    native_name = models.CharField(max_length = 5)
    phone_no = models.CharField(max_length = 10)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
    type = models.CharField(
        max_length=20, choices=Types.choices, default=Types.Emp
    )