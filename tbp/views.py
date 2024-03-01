
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import TravelerLoginForm, TravelerRegistrationForm
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import TravelerUpdateForm
# from .forms import FlightBookingForm
# from .models import Airline, BookedFlight, Plane



# Create your views here.


def home(request):
    return render(request,'home.html',{})

def register(request):
    if request.method == 'POST':
        form = TravelerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  # Redirect to the home page after successful registration
    else:
        form = TravelerRegistrationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = TravelerLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to a success page.
    else:
        form = TravelerLoginForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home') 

# Import the custom user model
from .models import traveler

def reset_password(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        new_password = request.POST.get('new_password')
        try:
            
            user = traveler.objects.get(username=username)
            user.set_password(new_password)
            user.save()
            update_session_auth_hash(request, user)  
            messages.success(request, 'Your password has been successfully updated.')
            return redirect('home')  
        except traveler.DoesNotExist:

            messages.error(request, 'User does not exist.')
            return redirect('reset_password')  

    return render(request, 'reset_password.html')  


def update_profile(request):
    if request.method == 'POST':
        form = TravelerUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile_updated')  # Redirect to a success page
    else:
        form = TravelerUpdateForm(instance=request.user)
    return render(request, 'update_profile.html', {'form': form})

def profile_updated(request):
    return render(request, 'profile_updated.html')


@login_required  # Ensures that only logged-in users can access this view
def view_profile(request):
    # Retrieve the traveler instance associated with the logged-in user
    profile = request.user

    # Pass the profile information to the template
    return render(request, 'profile.html', {'profile': profile})

from django.shortcuts import render, redirect
from django.contrib import messages  # Import messages module

from .forms import BookingForm
from .models import SeatBooking



# views.py
from django.shortcuts import render, redirect
from .forms import BookingForm
from .models import SeatBooking


# views.py
from django.shortcuts import render, redirect
from django.contrib import messages  # Import the messages module
from .forms import BookingForm
from .models import SeatBooking

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import BookingForm

def book_flight(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            # Process the form data and save the booking
            airline = form.cleaned_data['airlines']
            plane = form.cleaned_data['planes']
            seat = form.cleaned_data['seats']
            departure_country = form.cleaned_data['departure_country']
            arrival_country = form.cleaned_data['arrival_country']
            date = form.cleaned_data['date']

            try:
                booking = SeatBooking.objects.create(
                    seat=seat,
                    user=request.user,  # Assuming the user is authenticated
                    date=date,
                )
            except ValidationError as e:
                messages.error(request, e.message)
                return redirect('book_flight')

            # Redirect to a confirmation page or any other page
            messages.success(request, 'Booking successful!')
            return redirect('booking_confirmation')  # Adjust the URL name as needed
        else:
            # If form is not valid, re-render the form with error messages
            messages.error(request, 'This seat is already booked for the selected date.')
    else:
        form = BookingForm()

    return render(request, 'book_flight.html', {'form': form})




# def book_flight(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             # Process the form data and save the booking
#             airline = form.cleaned_data['airlines']
#             plane = form.cleaned_data['planes']
#             seat = form.cleaned_data['seats']
#             departure_country = form.cleaned_data['departure_country']
#             arrival_country = form.cleaned_data['arrival_country']
#             date = form.cleaned_data['date']

#             # Save the booking to the database
#             booking = SeatBooking.objects.create(
#                 seat=seat,
#                 user=request.user,  # Assuming the user is authenticated
#                 date=date,
#                 departure_country=departure_country,
#                 arrival_country=arrival_country
#             )
#             # Pass the booking object to the template
#             return render(request, 'booking_confirmation.html', {'booking': booking})
#     else:
#         form = BookingForm()
#     return render(request, 'book_flight.html', {'form': form})

# def book_flight(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             # Process the form data and save the booking
#             airline = form.cleaned_data['airlines']
#             plane = form.cleaned_data['planes']
#             seat = form.cleaned_data['seats']
#             departure_country = form.cleaned_data['departure_country']
#             arrival_country = form.cleaned_data['arrival_country']
#             date = form.cleaned_data['date']

#             # Save the booking to the database
#             booking = SeatBooking.objects.create(
#                 seat=seat,
#                 user=request.user,  # Assuming the user is authenticated
#                 date=date,
#             )
#             # Redirect to the booking confirmation page
#             return redirect('booking_confirmation')  # Adjust the URL name as needed
#         else:
#             # If form is not valid, display error message
#             messages.error(request, 'This seat is already booked for the selected date.')
#     else:
#         form = BookingForm()
        
#     return render(request, 'book_flight.html', {'form': form})




# from django.shortcuts import render, redirect
# from .forms import BookingForm
# from .models import SeatBooking


# def book_flight(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():  # This line triggers the form validation
#             # Process the form data and save the booking
#             airline = form.cleaned_data['airlines']
#             plane = form.cleaned_data['planes']
#             seat = form.cleaned_data['seats']
#             departure_country = form.cleaned_data['departure_country']
#             arrival_country = form.cleaned_data['arrival_country']
#             date = form.cleaned_data['date']

#             # Save the booking to the database
#             booking = SeatBooking.objects.create(
#                 seat=seat,
#                 user=request.user,  # Assuming the user is authenticated
#                 date=date,
#             )
#             # Redirect to a confirmation page or any other page
#             return redirect('booking_confirmation')  # Adjust the URL name as needed
#     else:
#         form = BookingForm()
        
#     return render(request, 'book_flight.html', {'form': form})


# def book_flight(request):
#     error_message = None
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             airline = form.cleaned_data['airlines']
#             plane = form.cleaned_data['planes']
#             seat = form.cleaned_data['seats']
#             departure_country = form.cleaned_data['departure_country']
#             arrival_country = form.cleaned_data['arrival_country']
#             date = form.cleaned_data['date']

#             # Check if the selected seat on the selected date is already booked
#             existing_bookings = SeatBooking.objects.filter(seat=seat, date=date)
#             if existing_bookings.exists():
#                 error_message = 'This seat is already booked for the selected date.'
#             else:
#                 # Save the booking to the database
#                 booking = SeatBooking.objects.create(
#                     seat=seat,
#                     user=request.user,  # Assuming the user is authenticated
#                     date=date,
#                 )
#                 # Redirect to a confirmation page or any other page
#                 return redirect('booking_confirmation')  # Adjust the URL name as needed
#     else:
#         form = BookingForm()
#     return render(request, 'book_flight.html', {'form': form, 'error_message': error_message})



from django.shortcuts import render

def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')
