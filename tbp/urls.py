from django.urls import path
from . import views
from .views import booking_confirmation, register, login_view
from .views import view_profile





urlpatterns = [
    path('', views.home,name= "home"),
    path('signup/', register, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('update_profile/', views.update_profile, name='update_profile'),
    path('profile_updated/', views.profile_updated, name='profile_updated'),
    path('profile/', view_profile, name='view_profile'),
    path('book-flight/', views.book_flight, name='book_flight'),
    path('booking-confirmation/', booking_confirmation, name='booking_confirmation'),

    ]
