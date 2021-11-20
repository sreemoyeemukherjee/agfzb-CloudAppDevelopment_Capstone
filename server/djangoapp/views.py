from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
from .restapis import get_dealers_from_cf, get_dealers_by_state_from_cf, get_dealer_reviews_from_cf, post_request
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json
import random

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    # If the request method is GET
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    # Handles POST request
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('/djangoapp')
        else:
            # If not, return to login page again
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    # Get the user object based on session id in request
    print("Log out the user `{}`".format(request.user.username))
    # Logout user in the request
    logout(request)
    # Redirect user back to course list view
    return redirect('/djangoapp')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("/djangoapp")
        else:
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = dict()
        url = "https://b2918b6e.us-south.apigw.appdomain.cloud/capstone/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

def get_dealerships_by_state(request, state):
    if request.method == "GET":
        url = "https://b2918b6e.us-south.apigw.appdomain.cloud/capstone/api/dealership"
        # Get dealers from the URL
        dealerships = get_dealers_by_state_from_cf(url, state)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render the reviews of a dealer
def get_dealer_details(request, dealer_id):
    if request.method == "GET":
        context = dict()
        url = "https://b2918b6e.us-south.apigw.appdomain.cloud/capstone/api/review"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        context['dealer_id'] = dealer_id
        dealer_names=""
        # Concat all dealer's short name
        for review in reviews:
            dealer_names = dealer_names + ' ' + review.review
            dealer_names = dealer_names + ' ' + review.sentiment
        # Return a list of dealer short name
        return render(request, 'djangoapp/dealer_details.html', context)

# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    context = dict()
    context['dealer_id'] = dealer_id
    url = "https://b2918b6e.us-south.apigw.appdomain.cloud/capstone/api/dealership"
    # Get dealers from the URL
    dealerships = get_dealers_from_cf(url)
    for d in dealerships:
        if(d.id == dealer_id):
            context['dealership'] = d.full_name
    if request.method == "GET":
        url = "https://b2918b6e.us-south.apigw.appdomain.cloud/capstone/api/review"
        # Get reviews from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        return render(request, 'djangoapp/dealer_details.html', context)

    elif request.user.is_authenticated and request.method == "POST":
        url= "https://b2918b6e.us-south.apigw.appdomain.cloud/capstone/api/review"
        review=dict()
        json_payload=dict()
        #review["time"] = datetime.utcnow().isoformat()
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        review["id"] = random.randint(2000, 3000)
        review["name"] = request.user.username
        review["dealership"] = dealer_id
        review["review"] = request.POST.get("content", False)
        if request.POST.get("purchasecheck", False) == 'on':
            review["purchase"] = True
            review["purchase_date"] = request.POST.get("purchasedate", False)
            for r in reviews:
                if int(r.id) == int(request.POST["car"]):
                    review["car_make"] = r.car_make
                    review["car_model"] = r.car_model                  
                    review["car_year"] = r.car_year
        else:
            review["purchase"] = False
            review["purchase_date"] = ""
            review["car_make"] = ""
            review["car_model"] = ""               
            review["car_year"] = ""
        # another = dict["review"]["another"]
        
        review["another"] = ""
        #review["car_model"] = request.POST.get("car", False)
        #review["car_year"] = request.POST.get("car", False)
        json_payload["review"] = review
        #print("DATA TO BE POSTED: ", json_payload['review'])
        if(review["review"] != False):
            data = post_request(url, json_payload, dealerId=dealer_id)
            return redirect("djangoapp:add_review", dealer_id=dealer_id)
    return render(request, 'djangoapp/add_review.html', context)
