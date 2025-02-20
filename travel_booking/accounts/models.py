from django.db import models
from django.contrib.auth.models import User

# Flight Model
class Flight(models.Model):
    airline = models.CharField(max_length=100)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    departure_date = models.DateField()
    departure_time = models.TimeField()

    def __str__(self):
       return f"{self.airline} - {self.departure} to {self.destination}"

# Hotel Model
class Hotel(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(default=0.0)
    image = models.ImageField(upload_to='hotels/', blank=True, null=True)

    def __str__(self):
        return f"{self.name} - {self.location}"

# Travel Package Model
class TravelPackage(models.Model):
    name = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='packages/')
    description = models.TextField()

    def __str__(self):
        return self.name

# User Profile Model
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    def __str__(self):
        return self.user.username
