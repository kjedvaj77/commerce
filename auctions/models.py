from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    title = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    description = models.CharField(max_length=1500)
    image = models.CharField(max_length=1500)
    startingPrice = models.FloatField()
    sold = models.BooleanField(default=False)
    watchlist = models.ManyToManyField(User, blank=True, null=True, name='watchlist')

    def __str__(self):
        return self.title
    

class Bid(models.Model):
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bids')
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name='bids')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"User: {self.bidder} Amount:{self.amount} Auction:{self.auction}"


