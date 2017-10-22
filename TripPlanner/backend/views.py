from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Trip, City, Destination
import sys


LOGIN_URL = '/site/login/'


def index(request):
    return render(request, 'backend/index.html', {'username': request.user.username})


@login_required(login_url=LOGIN_URL)
def dashboard(request):
    trips = []
    for trip in Trip.get_trips_of_user(request.user):
        data = trip.get_data()
        cost = trip.total_weight(trip.traveling_salesman(trip.get_data()['destinations'][-1]['city']))
        if cost['sum'] == sys.maxsize:
            cost['sum'] = 0
        trips.append({
            'data': data,
            'money': cost,
        })
    return render(request, 'backend/dashboard.html', {'trips': trips, 'username': request.user.username})


@login_required(login_url=LOGIN_URL)
def create_trip(request):
    trip_name = request.POST.get('name', "")
    start_time = "{0}-{1}-{2}".format(request.POST.get('departure-year', ""), request.POST.get('departure-month', ""), request.POST.get('departure-day', ""))
    trip_date = datetime.strptime(start_time, '%Y-%m-%d')
    interval_time = "{0}-{1}-{2}".format(request.POST.get('arrival-year', ""), request.POST.get('arrival-month', ""), request.POST.get('arrival-day', ""))
    interval = datetime.strptime(interval_time, '%Y-%m-%d')
    start_city = City.get_or_add(request.POST.get('departure-from', ''))
    trip = Trip(name=trip_name, user=request.user, start_day=trip_date, start_city=start_city, interval=interval)
    trip.save()
    city_names = request.POST.getlist('destinations[]', [])
    city_days = request.POST.getlist('destination-durations[]', [])

    for (name, days) in zip(city_names, city_days):
        city = City.get_or_add(name)
        if city is None:
            return HttpResponse("Invalid city name (no api response)")
        else:
            destination = Destination(trip=trip, city=city, planned_days=days)
            destination.save()

    print("Saving")
    return HttpResponseRedirect("/site/dashboard")


def user_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")
    next = request.GET.get('next', "/site/dashboard")
    print(next)
    errors = []
    if username != "":
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(str(next))
        else:
            errors.append("Username or password incorrect")
    return render(request, 'backend/login.html', {'errors': errors, 'next': next, 'username': request.user.username})


def user_registration(request):
    firstname = request.POST.get('first_name', "")
    lastname = request.POST.get('last_name', "")
    username = request.POST.get('username', "")
    email = request.POST.get('email', "")
    password = request.POST.get('password', "")
    password_again = request.POST.get('password_again', "")
    if username == "":
        return render(request, 'backend/register.html', {'username': request.user.username})

    users = User.objects.all()

    if users.filter(username=username).exists():
        return HttpResponse("Username is already taken.")

    for user in users:
        if user.email == email:
            return HttpResponse("You already registered with another email address.")

    if password != password_again:
        return HttpResponse("Password mismatch detected.")

    User.objects.create_user(username=username, email=email,
                             first_name=firstname, last_name=lastname, password=password)
    return HttpResponseRedirect("/site/login")

@login_required(login_url=LOGIN_URL)
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/site")
