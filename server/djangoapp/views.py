from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealer_by_id_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from datetime import datetime
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {
        "title": "About us"
    }
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {
        "title": "Contact us"
    }
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/user_login.html', context)
    else:
        return render(request, 'djangoapp/user_login.html', context)


# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {
        "title": "Register"
    }
    if request.method == 'GET':
        return render(request, 'djangoapp/user_registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/user_registration.html', context)


# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {
        "title": "Our Dealerships"
    }

    if request.method == "GET":
        url = "https://f65a6699.eu-gb.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context["dealership_list"] = dealerships

        return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    context = {
        "title": "Dealership Details"
    }

    if request.method == "GET":
        url = "https://f65a6699.eu-gb.apigw.appdomain.cloud/api/review"
        # Get dealers from the URL
        dealerships = get_dealer_by_id_from_cf(url, dealer_id)
        context["dealer_details"] = dealerships
        context["dealer_id"] = dealer_id

        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = {
        "title": "Write Review"
    }

    if request.method == 'GET':
        url = "https://f65a6699.eu-gb.apigw.appdomain.cloud/api/dealership"
        dealer = get_dealers_from_cf(url, dealerId=dealer_id)
        context["dealer"] = dealer[0]

        cars = CarModel.objects.filter(dealerID=dealer_id)
        context["cars"] = cars

        return render(request, 'djangoapp/add_review.html', context)
    else:
        url = "https://f65a6699.eu-gb.apigw.appdomain.cloud/api/review"
        
        if request.user.is_authenticated:
            review = {}
            review["time"] = datetime.utcnow().isoformat()
            review["name"] = request.user.username
            review["dealership"] = int(dealer_id)
            review["review"] = request.POST["content"]
            review["purchase"] = False

            if request.POST.get("purchasecheck") and request.POST["purchasecheck"] == 'on':
                review["purchase"] = True
                review["purchase_date"] = request.POST["purchasedate"]
                
                if(request.POST.get("car")):
                    carId= request.POST["car"]
                    car = CarModel.objects.get(pk=carId)
                    
                    review["car_make"] = car.carMake.name
                    review["car_model"] = car.name
                    review["car_year"] = car.year

            json_payload = {"review" : review }

            post_request(url, json_payload)

        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)

