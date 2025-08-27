from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
        ('manager', 'Manager'),
    )
    ID_TYPES = (
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
    )
    GENDERS = (
        ('male', 'Male'),
        ('female', 'Female'),
    )

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    id_type = models.CharField(max_length=20, choices=ID_TYPES, blank=True)
    id_number = models.CharField(max_length=50, blank=True)
    gender = models.CharField(max_length=10, choices=GENDERS, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f"{self.email} ({self.role})"
