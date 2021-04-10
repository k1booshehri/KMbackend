from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.IntegerField(null=True, unique=True)
    email = models.EmailField(null=True, max_length=254, unique=True)
    profile_image = models.ImageField(blank=True, null=True)
    university = models.CharField(null=True, max_length=300)
    field_of_study = models.CharField(null=True, max_length=400)
    entry_year = models.IntegerField(null=True)


class Book(models.Model):
    title = models.CharField(null=True, max_length=300)
    author = models.CharField(null=True, max_length=300)
    publisher = models.CharField(null=True, max_length=300)
    image = models.ImageField(blank=True, null=True)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
