
from django.forms import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import TravelerLoginForm, TravelerRegistrationForm
from .forms import BookRoomForm,BookVehicleForm
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import TravelerUpdateForm
from .models import Hotel,Room,Vehicle,Agency
from .forms import AdvancedSearchForm,AdvancedCarSearchForm,BookRoom,BookVehicle
from django.utils import timezone
from django.db.models import Prefetch
from .models import SeatBooking, Plane
from .forms import SearchForm
from .forms import BookingForm
from django.shortcuts import get_object_or_404






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

# views.py

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

@login_required
def book_room(request):
    if request.method == 'POST':
        form = BookRoomForm(request.POST)
        if form.is_valid():
            book_room = form.save(commit=False)
            book_room.traveler = request.user  # Assign the logged-in user as the traveler
            book_room.save()
            return redirect('booking_confirmation')  # Redirect to booking confirmation page
    else:
        form = BookRoomForm()
    return render(request, 'book_room.html', {'form': form})

@login_required
def book_vehicle(request):
    if request.method == 'POST':
        form = BookVehicleForm(request.POST)
        if form.is_valid():
            book_vehicle = form.save(commit=False)
            book_vehicle.traveler = request.user  # Assign the logged-in user as the traveler
            book_vehicle.save()
            return redirect('booking_confirmation')  # Redirect to booking confirmation page
    else:
        form = BookVehicleForm()
    return render(request, 'book_vehicle.html', {'form': form})

def booking_confirmation_view(request):
    return render(request, 'booking_confirmation.html')


def hotels_list(request):
    hotels = Hotel.objects.prefetch_related('room_set').all()  # Retrieve hotels with related rooms
    return render(request, 'hotels_list.html', {'hotels': hotels})

def agencies_list(request):
    agencies = Agency.objects.prefetch_related('vehicle_set').all()
    return render(request, 'agencies_list.html', {'agencies': agencies})

def advanced_search(request):
    form = AdvancedSearchForm(request.GET)
    hotels = []
    if form.is_valid():
        hotels = form.filter_hotels()
    return render(request, 'advanced_search.html', {'form': form, 'hotels': hotels})

def advanced_car_search(request):
    form = AdvancedCarSearchForm(request.GET)
    agencies = []
    if form.is_valid():
        agencies = form.filter_agencies()
    return render(request, 'advanced_car_search.html', {'form': form, 'agencies': agencies})

def booked_rooms(request):
    today = timezone.now().date()
    past_booked_rooms = BookRoom.objects.filter(traveler=request.user, checkout_date__lt=today).select_related('room__hotel')
    upcoming_booked_rooms = BookRoom.objects.filter(traveler=request.user, booking_date__gte=today).select_related('room__hotel')
    current_booked_rooms = BookRoom.objects.filter(
        traveler=request.user,
        booking_date__lte=today,
        checkout_date__gte=today
    ).select_related('room__hotel')

    return render(request, 'booked_rooms.html', {
        'past_booked_rooms': past_booked_rooms,
        'upcoming_booked_rooms': upcoming_booked_rooms,
        'current_booked_rooms': current_booked_rooms
    })
    
def booked_vehicles(request):
    today = timezone.now().date()
    past_booked_vehicles = BookVehicle.objects.filter(traveler=request.user, checkout_date__lt=today).select_related('vehicle__agency')
    upcoming_booked_vehicles = BookVehicle.objects.filter(traveler=request.user, booking_date__gte=today).select_related('vehicle__agency')
    current_booked_vehicles = BookVehicle.objects.filter(
        traveler=request.user,
        booking_date__lte=today,
        checkout_date__gte=today
    ).select_related('vehicle__agency')

    return render(request, 'booked_vehicles.html', {
        'past_booked_vehicles': past_booked_vehicles,
        'upcoming_booked_vehicles': upcoming_booked_vehicles,
        'current_booked_vehicles': current_booked_vehicles
    })    
    
#Ishan's code

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

def booking_confirmation(request):
    return render(request, 'booking_confirmation.html')

def search_vacant_seats(request):
    form = SearchForm(request.GET)

    if form.is_valid():
        airline = form.cleaned_data.get('airline')
        plane = form.cleaned_data.get('plane')
        date = form.cleaned_data.get('date')

        if plane is not None:
            # Get all seats from the specified plane
            all_seats = plane.seat_set.all()

            # Filter seats that are not booked on the specified date
            booked_seats = SeatBooking.objects.filter(date=date, seat__in=all_seats).values_list('seat', flat=True)
            vacant_seats = all_seats.exclude(id__in=booked_seats)

            return render(request, 'vacant_seats.html', {'form': form, 'vacant_seats': vacant_seats})

    return render(request, 'search_vacant_seats.html', {'form': form})

def view_flight_details(request, flight_id):
    # Retrieve the specific flight using the flight_id
    flight = get_object_or_404(Plane, pk=flight_id)

    # You can customize this rendering based on your model structure
    return render(request, 'flight_details.html', {'flight': flight})

def home(request):
    available_flights = Plane.objects.all()  # Update this query as needed
    return render(request, 'home.html', {'available_flights': available_flights})

def view_all_flight_details(request):
    all_flights = Plane.objects.all()  # Retrieve all flights from the database
    return render(request, 'all_flight_details.html', {'all_flights': all_flights})