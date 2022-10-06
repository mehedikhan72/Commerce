from codecs import charmap_build
from email.policy import default
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone

class Listing(models.Model):
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=1024)
    price = models.FloatField()
    image_url = models.CharField(max_length=2048)
    category = models.CharField(max_length=64)
    listed_by = models.CharField(max_length=64)
    created = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now)
    bid_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"

class User(AbstractUser):
    watchlist=models.ManyToManyField(Listing, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.username}"

class Comment(models.Model):
    comm = models.CharField(max_length=4048, default=None)
    comm_item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comm_item", default=None)
    comm_person = models.ForeignKey(User, to_field="username", db_column="username", on_delete=models.CASCADE, related_name="comm_person", default=None)
    commented = models.DateField(auto_now_add=False, auto_now=False, default=timezone.now)
    def __str__(self):
        return f"{self.comm}"

class Bid(models.Model):
    id = models.AutoField(primary_key=True)
    bid_item = models.CharField(max_length=64)
    starting_bid = models.FloatField()
    current_bid = models.FloatField()
    current_bidder = models.CharField(max_length=64, null=True)
    first_bid_made = models.BooleanField(default=False)
    bid_closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.bid_item} currently costs {self.current_bid}"