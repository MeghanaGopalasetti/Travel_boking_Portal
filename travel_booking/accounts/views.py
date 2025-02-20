from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import razorpay
from django.conf import settings
#  Logout User
def user_logout(request):
    logout(request)
    messages.success(request, "Logout successfully.")
    return redirect('login')

#  Home Page (Redirect to Dashboard if Logged In)
def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

#  User Login
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')  # Redirect to dashboard after login
        messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

#  User Registration
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect('register')

        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, "Account created successfully! Please log in.")
        return redirect('login')

    return render(request, 'register.html')

#  Dashboard (After Login)
@login_required
def dashboard(request):
    return render(request, 'dashboard.html')

#  Flight Search Page
@login_required
def flights(request):
    """Displays flight search page and handles search queries."""
    search_query = request.GET.get('destination', '')  # Get search input

    flights_data = [
        {"airline": "Air India", "from": "Delhi", "to": "Mumbai", "price": "2500"},
        {"airline": "IndiGo", "from": "Delhi", "to": "Bangalore", "price": "3000"},
        {"airline": "SpiceJet", "from": "Mumbai", "to": "Goa", "price": "2200"},
        {"airline": "Vistara", "from": "Chennai", "to": "Delhi", "price": "1800"},
        {"airline": "GoAir", "from": "Kolkata", "to": "Chennai", "price": "2200"},
        {"airline": "Air India", "from": "Hyderabad", "to": "Kolkata", "price": "3190"},
        {"airline": "IndiGo", "from": "Bangalore", "to": "Hyderabad", "price": "2400"},
        {"airline": "SpiceJet", "from": "Delhi", "to": "Jaipur", "price": "3000"},
        {"airline": "Vistara", "from": "Mumbai", "to": "Chennai", "price": "1760"},
        {"airline": "GoAir", "from": "Pune", "to": "Bangalore", "price": "1780"},
        {"airline": "Air Asia", "from": "Kolkata", "to": "Delhi", "price": "2510"},
        {"airline": "IndiGo", "from": "Chennai", "to": "Goa", "price": "3130"},
        {"airline": "SpiceJet", "from": "Hyderabad", "to": "Mumbai", "price": "3275"},
        {"airline": "Vistara", "from": "Delhi", "to": "Kolkata", "price": "2230"},
        {"airline": "GoAir", "from": "Bangalore", "to": "Jaipur", "price": "3145"},
        {"airline": "Air India", "from": "Jaipur", "to": "Goa", "price": "2190"},
        {"airline": "IndiGo", "from": "Pune", "to": "Delhi", "price": "2195"},
        {"airline": "SpiceJet", "from": "Chennai", "to": "Bangalore", "price": "1510"},
        {"airline": "Vistara", "from": "Mumbai", "to": "Hyderabad", "price": "1550"},
        {"airline": "GoAir", "from": "Delhi", "to": "Pune", "price": "2175"},
    ]

    # Filter flights based on search query
    if search_query:
        flights_data = [flight for flight in flights_data if search_query.lower() in flight['to'].lower()]

    return render(request, 'flights.html', {"flights": flights_data, "search_query": search_query})

#  Hotel Search Page
@login_required
def hotels(request):
    search_city = request.GET.get('city', '')
    hotels_data = [
        {"name": "The Taj", "location": "Mumbai", "price": "3000"},
        {"name": "Leela Palace", "location": "Delhi", "price": "2500"},
        {"name": "Oberoi Grand", "location": "Kolkata", "price": "2200"},
        {"name": "ITC Grand Chola", "location": "Chennai", "price": "2800"},
        {"name": "Hyatt Regency", "location": "Bangalore", "price": "2600"},
        {"name": "Radisson Blu", "location": "Hyderabad", "price": "2400"},
        {"name": "Marriott Hotel", "location": "Pune", "price": "2700"},
        {"name": "The Oberoi", "location": "Udaipur", "price": "3500"},
        {"name": "JW Marriott", "location": "Goa", "price": "3200"},
        {"name": "Vivanta by Taj", "location": "Jaipur", "price": "2300"},
        {"name": "The Lalit", "location": "Chandigarh", "price": "2100"},
        {"name": "The Park", "location": "Kolkata", "price": "1900"},
        {"name": "Taj Falaknuma", "location": "Hyderabad", "price": "4000"},
        {"name": "The Leela Kovalam", "location": "Kerala", "price": "2800"},
        {"name": "Grand Hyatt", "location": "Mumbai", "price": "3100"},
        {"name": "Fairmont", "location": "Jaipur", "price": "2900"},
        {"name": "The Westin", "location": "Gurgaon", "price": "2750"},
        {"name": "Trident", "location": "Chennai", "price": "2600"},
        {"name": "ITC Rajputana", "location": "Jaipur", "price": "2200"},
        {"name": "Holiday Inn", "location": "Goa", "price": "1800"},
    ]

    # Filter hotels based on search query
    if search_city:
        hotels_data = [hotel for hotel in hotels_data if search_city.lower() in hotel['location'].lower()]

    return render(request, 'hotels.html', {"hotels": hotels_data, "search_city": search_city})

#  Travel Packages Page
@login_required
def packages(request):
    packages_data = [
        {
            "name": "Goa Beach Escape",
            "destination": "Goa",
            "price": "₹000",
            "image": "images/goa.jpg"
        },
        {
            "name": "Kashmir Winter Wonderland",
            "destination": "Kashmir",
            "price": "7500",
            "image": "images/kashmir.jpg"
        },
        {
            "name": "Kerala Backwaters",
            "destination": "Kerala",
            "price": "6000",
            "image": "images/kerala.jpg"
        },
        {
            "name": "Royal Rajasthan Tour",
            "destination": "Jaipur, Udaipur, Jaisalmer",
            "price": "9000",
            "image": "images/rajasthan.jpg"
        },
        {
            "name": "Himalayan Adventure",
            "destination": "Manali, Leh, Ladakh",
            "price": "6100",
            "image": "images/ladakh.jpg"
        },

    ]

    return render(request, 'packages.html', {"packages": packages_data})

def payment(request):
    booking_type = request.GET.get('booking_type', '')
    booking_details = request.GET.get('booking_details', '')
    price = request.GET.get('price', '')

    return render(request, 'payment.html', {
        'booking_type': booking_type,
        'booking_details': booking_details,
        'price': price
    })

#  Razorpay client
client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

def process_payment(request):
    if request.method == "POST":
        booking_type = request.POST.get('booking_type', '')
        booking_details = request.POST.get('booking_details', '')
        price_str = request.POST.get('price', '1').strip()
        price_str = price_str.replace("₹", "").replace(",", "").strip()

        try:
            price = int(price_str) * 100
        except ValueError:
            return redirect('/payment?error=invalid_price')

        order_data = {
            "amount": price,
            "currency": "INR",
            "payment_capture": price
        }
        order = client.order.create(data=order_data)

        return render(request, "payment.html", {
            "order_id": order["id"],
            "amount": price // 100,
            "key": "rzp_test_ZkmFIsQ6R9GcAS",
            "booking_type": booking_type,
            "booking_details": booking_details
        })

    return redirect('/dashboard')

def payment_success(request):
    return render(request, "payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")


















