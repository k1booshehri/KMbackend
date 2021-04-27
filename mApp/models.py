from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.IntegerField(null=True, unique=True)
    email = models.EmailField(null=True, max_length=254, unique=True)
    profile_image = models.ImageField(blank=True, null=True)
    university = models.CharField(null=True, max_length=300, blank=True)
    field_of_study = models.CharField(null=True, max_length=400, blank=True)
    entry_year = models.IntegerField(null=True, blank=True)


class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(null=True, max_length=300)
    author = models.CharField(null=True, max_length=300)
    publisher = models.CharField(null=True, max_length=300)
    price = models.IntegerField(null=True)
    province = models.CharField(null=True, max_length=100)
    city = models.CharField(null=True, max_length=100)
    zone = models.CharField(null=True, max_length=100)
    status = models.CharField(null=True, max_length=100)
    description = models.CharField(null=True, max_length=100)
    is_active = models.BooleanField(null=True)
    image = models.ImageField(blank=True, null=True)
    categories = models.CharField(null=True, max_length=500)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def get_city(self):
        return self.title + ' is in ' + self.city + ' city.'


class Bid(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    offered_price = models.IntegerField(null=True, max_length=8)
    description = models.CharField(null=True, max_length=500)
