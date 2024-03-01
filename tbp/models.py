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
   

#Ishan's code

class Airline(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Plane(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.airline.name} - {self.name}"
    

User = get_user_model()

class Seat(models.Model):
    plane = models.ForeignKey(Plane, on_delete=models.CASCADE)
    seat_number = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.plane.name} - Seat {self.seat_number}"

class SeatBooking(models.Model):
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField()

    def clean(self):
        # Check if there's already a booking for the same seat on the same date
        existing_bookings = SeatBooking.objects.filter(seat=self.seat, date=self.date)
        if self.pk:
            existing_bookings = existing_bookings.exclude(pk=self.pk)
        if existing_bookings.exists():
            raise ValidationError('Another booking exists for this seat on the same date.')

    def __str__(self):
        return f"{self.user.username} - {self.seat} - {self.date}"