from django.urls import path
from . import views
from .views import register, login_view
from .views import view_profile,booking_confirmation_view



urlpatterns = [
    path('', views.home,name= "home"),
    path('signup/', register, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile_updated/', views.profile_updated, name='profile_updated'),
    path('profile/', view_profile, name='view_profile'),
    path('book_room/', views.book_room, name='book_room'),
    path('booking-confirmation/', booking_confirmation_view, name='booking_confirmation'), 
    path('hotels/', views.hotels_list, name='hotels_list'),
    path('advanced-search/', views.advanced_search, name='advanced_search'),
    path('book_vehicle/', views.book_vehicle, name='book_vehicle'),
    path('advanced-car-search/', views.advanced_car_search, name='advanced_car_search'),
    path('Agencies/', views.agencies_list, name='agencies_list'),
    path('booked_rooms/', views.booked_rooms, name='booked_rooms'),
    path('booked_vehicles/', views.booked_vehicles, name='booked_vehicles'),
    
    ]
