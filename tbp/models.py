from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError


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



