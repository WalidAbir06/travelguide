from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from .models import traveler
from django import forms
from .models import Airline, Plane



User = get_user_model()


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





# forms.py
from django import forms
from .models import Airline, Plane, Seat, SeatBooking

class BookingForm(forms.Form):
    airlines = forms.ModelChoiceField(queryset=Airline.objects.all(), label='Select Airline')
    planes = forms.ModelChoiceField(queryset=Plane.objects.all(), label='Select Plane')
    seats = forms.ModelChoiceField(queryset=Seat.objects.all(), label='Select Seat')
    departure_country = forms.CharField(label='Departure Country', max_length=100)
    arrival_country = forms.CharField(label='Arrival Country', max_length=100)
    date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))

    def clean(self):
        cleaned_data = super().clean()
        plane = cleaned_data.get('planes')
        seat = cleaned_data.get('seats')
        date = cleaned_data.get('date')
        departure_country = cleaned_data.get('departure_country')
        arrival_country = cleaned_data.get('arrival_country')

        if plane and seat and date and departure_country and arrival_country:
            existing_bookings = SeatBooking.objects.filter(seat=seat, date=date)
            if existing_bookings.exists():
                raise forms.ValidationError('This seat is already booked for the selected date.')


walid =  "ASS"

# forms.py
# from django import forms
# from .models import Airline, Plane, Seat, SeatBooking

# class BookingForm(forms.Form):
#     airlines = forms.ModelChoiceField(queryset=Airline.objects.all(), label='Select Airline')
#     planes = forms.ModelChoiceField(queryset=Plane.objects.all(), label='Select Plane')
#     seats = forms.ModelChoiceField(queryset=Seat.objects.all(), label='Select Seat')
#     departure_country = forms.CharField(label='Departure Country', max_length=100)
#     arrival_country = forms.CharField(label='Arrival Country', max_length=100)
#     # date = forms.DateField(label='Date')
#     date = forms.DateField(label='Date', widget=forms.DateInput(attrs={'type': 'date'}))

#     def clean(self):
#         cleaned_data = super().clean()
#         plane = cleaned_data.get('planes')
#         seat = cleaned_data.get('seats')
#         date = cleaned_data.get('date')

#         if plane and seat and date:
#             existing_bookings = SeatBooking.objects.filter(seat=seat, date=date)
#             if existing_bookings.exists():
#                 raise forms.ValidationError('This seat is already booked for the selected date.')
