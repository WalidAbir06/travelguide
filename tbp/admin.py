from django.contrib import admin
from . models import traveler, Hotel, Room, BookRoom, Agency, Vehicle,BookVehicle
from .models import Airline, Plane,Seat, SeatBooking

# Register your models here.
admin.site.register(traveler)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(BookRoom)
admin.site.register(Agency)
admin.site.register(Vehicle)
admin.site.register(BookVehicle)
#Ishan's code


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'airline', 'model', 'capacity')



admin.site.register(Seat)
admin.site.register(SeatBooking)
