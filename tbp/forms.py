from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django import forms
from .models import traveler
from .models import BookRoom,Room,Hotel,BookVehicle,Agency,Vehicle
from django.core.exceptions import ValidationError
User = get_user_model()
#Ishan's code
from .models import Airline, Plane, Seat, SeatBooking
from datetime import date

class TravelerRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.IntegerField(required=True)
    age = forms.IntegerField(required=True)
    name = forms.CharField(required=True)
    gender = forms.ChoiceField(choices=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])


    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'age', 'name', 'gender', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.phone = self.cleaned_data['phone']
        user.age = self.cleaned_data['age']
        user.name = self.cleaned_data['name']
        user.gender = self.cleaned_data['gender']
        if commit:
            user.save()
        return user
    
class TravelerLoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ('username', 'password')


class TravelerUpdateForm(forms.ModelForm):
    class Meta:
        model = traveler
        fields = ['email', 'phone', 'age', 'name', 'gender']
        
class BookRoomForm(forms.ModelForm):
    class Meta:
        model = BookRoom
        fields = ['room', 'booking_date', 'checkout_date']

    def clean(self):
        cleaned_data = super().clean()
        room = cleaned_data.get('room')
        booking_date = cleaned_data.get('booking_date')
        checkout_date = cleaned_data.get('checkout_date')

        if room and booking_date and checkout_date:
            existing_bookings = BookRoom.objects.filter(room=room)
            for booking in existing_bookings:
                if (booking.booking_date <= checkout_date) and (booking.checkout_date >= booking_date):
                    raise ValidationError('Another booking exists within this duration')

        return cleaned_data
    
class BookVehicleForm(forms.ModelForm):
    class Meta:
        model = BookVehicle
        fields = ['vehicle', 'booking_date', 'checkout_date']

    def clean(self):
        cleaned_data = super().clean()
        vehicle = cleaned_data.get('vehicle')
        booking_date = cleaned_data.get('booking_date')
        checkout_date = cleaned_data.get('checkout_date')

        if vehicle and booking_date and checkout_date:
            existing_bookings = BookVehicle.objects.filter(vehicle=vehicle)
            for booking in existing_bookings:
                if (booking.booking_date <= checkout_date) and (booking.checkout_date >= booking_date):
                    raise forms.ValidationError('Another booking exists within this duration')

        return cleaned_data
    
class AdvancedSearchForm(forms.Form):
    location = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    room_type = forms.ChoiceField(choices=Room.TYPE_CHOICES, required=False)

    def filter_hotels(self):
        queryset = Hotel.objects.all()

        location = self.cleaned_data.get('location')
        min_price = self.cleaned_data.get('min_price')
        max_price = self.cleaned_data.get('max_price')
        room_type = self.cleaned_data.get('room_type')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(room__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(room__price__lte=max_price)
        if room_type:
            queryset = queryset.filter(room__type=room_type)

        return queryset.distinct()
    
class AdvancedCarSearchForm(forms.Form):
    location = forms.CharField(required=False)
    min_price = forms.DecimalField(required=False, min_value=0)
    max_price = forms.DecimalField(required=False, min_value=0)
    car_type = forms.ChoiceField(choices=Vehicle.CAR_TYPE_CHOICES, required=False)

    def filter_agencies(self):
        queryset = Agency.objects.all()

        location = self.cleaned_data.get('location')
        min_price = self.cleaned_data.get('min_price')
        max_price = self.cleaned_data.get('max_price')
        car_type = self.cleaned_data.get('car_type')

        if location:
            queryset = queryset.filter(location__icontains=location)
        if min_price:
            queryset = queryset.filter(vehicle__price__gte=min_price)
        if max_price:
            queryset = queryset.filter(vehicle__price__lte=max_price)
        if car_type:
            queryset = queryset.filter(vehicle__car_type=car_type)

        return queryset.distinct()
    
#Ishan's code
class BookingForm(forms.Form):
    airlines = forms.ModelChoiceField(queryset=Airline.objects.all(), label='Select Airline')
    planes = forms.ModelChoiceField(queryset=Plane.objects.all(), label='Select Plane')
    seats = forms.ModelChoiceField(queryset=Seat.objects.all(), label='Select Seat')
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))
    departure_country = forms.CharField(max_length=100, label='Departure Country', required=False)
    arrival_country = forms.CharField(max_length=100, label='Arrival Country', required=False)

    def clean(self):
        cleaned_data = super().clean()

        # Get the selected seat and date
        selected_seat = cleaned_data.get('seats')
        selected_date = cleaned_data.get('date')

        # Check if the seat is already booked on the selected date
        if SeatBooking.objects.filter(seat=selected_seat, date=selected_date).exists():
            raise forms.ValidationError('This seat is already booked on the selected date.')

        return cleaned_data
class SearchForm(forms.Form):
    airline = forms.ModelChoiceField(queryset=Airline.objects.all(), required=False)
    plane = forms.ModelChoiceField(queryset=Plane.objects.all(), required=False)
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))