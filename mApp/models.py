from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_number = models.IntegerField(null=True, unique=True)
    email = models.EmailField(null=True, max_length=254, unique=True)
    profile_image = models.ImageField(blank=True, null=True)
    university = models.CharField(null=True, max_length=300, blank=True)
    field_of_study = models.CharField(null=True, max_length=400, blank=True)
    entry_year = models.IntegerField(null=True, blank=True)
    is_store=models.BooleanField(default=False)
    store_name=models.CharField(null=True, max_length=300, blank=True)


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
    is_active = models.BooleanField(null=True, default=True)
    image = models.ImageField(blank=True, null=True)
    categories = models.CharField(null=True, max_length=500)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    exchange_book_title = models.CharField(null=True, max_length=500)
    exchange_book_author = models.CharField(null=True, max_length=500)
    exchange_book_publisher = models.CharField(null=True, max_length=500)
    def get_city(self):
        return self.title + ' is in ' + self.city + ' city.'
    is_from_store=models.BooleanField(default=False)
    store_quantity=models.IntegerField(null=True, blank=True)


class Bid(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    offered_price = models.IntegerField(null=True)
    description = models.CharField(null=True, max_length=500)
    is_accepted = models.BooleanField(null=True, default=False)
    exchange_image = models.ImageField(blank=True, null=True)


class Notifications(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    message = models.CharField(null=True, max_length=1000)
    is_seen=models.BooleanField(default=False)

    
class ChatThread(models.Model):
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user1')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='user2')


class ChatMessage(models.Model):
    thread = models.ForeignKey(ChatThread, on_delete=models.CASCADE, null=True)
    message = models.CharField(null=True, max_length=1500)
    is_read = models.BooleanField(null=True, default=False)
    created_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='sender')
    reply_of = models.IntegerField(null=True)

    
class Bookmarks(models.Model):
    markedpost=models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    markedby=models.ForeignKey(User, on_delete=models.CASCADE, null=True)
