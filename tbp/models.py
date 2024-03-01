from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django import forms



# Create your models here.

class traveler(AbstractUser):
    username = models.CharField(max_length=150, primary_key=True)
    email = models.EmailField(unique=True)
    phone = models.IntegerField(null=True)
    age = models.PositiveIntegerField(null=True)
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.username
    
class Hotel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Room(models.Model):
    TYPE_CHOICES = [
        ('Standard', 'Standard'),
        ('Deluxe', 'Deluxe'),
        ('Suite', 'Suite'),
    ]

    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    room_number = models.CharField(max_length=20)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='Standard')

    class Meta:
        unique_together = ('hotel', 'room_number')  # Partial key constraint

    def __str__(self):
        return f"{self.get_type_display()} Room {self.room_number} at {self.hotel.name}"



class Agency(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Vehicle(models.Model):
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    CAR_TYPE_CHOICES = [
        ('Sedan', 'Sedan'),
        ('SUV', 'SUV'),
        ('Truck', 'Truck'),
        ('Van', 'Van'),
        ('Hatchback', 'Hatchback'),
        ('Convertible', 'Convertible'),
        ('Coupe', 'Coupe'),
    ]
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    car_type = models.CharField(max_length=100, choices=CAR_TYPE_CHOICES)
    license_no = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.car_type} ({self.license_no}) - {self.agency.name}"
    

class BookVehicle(models.Model):
    traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, null=True)
    booking_date = models.DateField()
    checkout_date = models.DateField()

    def __str__(self):
        return f"{self.traveler.username}'s Booking from {self.booking_date} to {self.checkout_date}"
    
class BookRoom(models.Model):
    traveler = models.ForeignKey('Traveler', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=True)
    booking_date = models.DateField()
    checkout_date = models.DateField()

    def __str__(self):
       return f"{self.traveler.username}'s Booking from {self.booking_date} to {self.checkout_date}"
   

