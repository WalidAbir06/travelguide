from django.contrib import admin
from . models import traveler, Hotel, Room, BookRoom, Agency, Vehicle,BookVehicle

# Register your models here.
admin.site.register(traveler)
admin.site.register(Hotel)
admin.site.register(Room)
admin.site.register(BookRoom)
admin.site.register(Agency)
admin.site.register(Vehicle)
admin.site.register(BookVehicle)