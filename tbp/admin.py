from django.contrib import admin
from . models import  Seat, SeatBooking, traveler
from django.contrib import admin
from .models import Airline, Plane
# from .models import BookedFlight

# Register your models here.
admin.site.register(traveler)


@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'country')

@admin.register(Plane)
class PlaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'airline', 'model', 'capacity')



admin.site.register(Seat)
admin.site.register(SeatBooking)
