from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.IntegerField(null=True, unique=True)
    email = models.EmailField(null=True, max_length=254, unique=True)
    profile_image = models.ImageField(blank=True, null=True)
    university = models.CharField(null=True, max_length=300)
    field_of_study = models.CharField(null=True, max_length=400)
    entry_year = models.IntegerField(null=True)
