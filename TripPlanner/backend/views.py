from django.contrib.auth.models import User
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from datetime import datetime
from .models import Trip, City, Destination


def index(request):
    return render(request, 'backend/index.html')


@login_required(login_url='/site/login/')
def dashboard(request):
    trips = [trip.get_data() for trip in Trip.get_trips_of_user(request.user)]
    return render(request, 'backend/dashboard.html', {'trips': trips, 'username': request.user.username})


@login_required(login_url='/site/login/')
def create_trip(request):
    trip_name = request.POST.get('trip_name', "")
    trip_date = datetime.strptime(request.POST.get('trip_date', ""), '%Y-%m-%d')
    start_city = City.get_or_add(request.POST.get('start_city', ''))
    trip = Trip(name=trip_name, user=request.user, start_day=trip_date)
    city_names = request.POST.getlist('cities[]', [])
    city_days = request.POST.getlist('days[]', [])

    for name, days in zip(city_names, city_days):
        city = City.get_or_add(name)
        if city is None:
            return HttpResponse("Invalid city name (no api response)")
        else:
            destination = Destination(trip=trip, city=city, planned_days=days)
            destination.save()

    trip.save()
    return HttpResponse("Ok.")


def user_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")
    next = request.GET.get('next', "/site")
    print(next)
    errors = []
    if username != "":
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(str(next))
        else:
            errors.append("Username or password incorrect")
    return render(request, 'backend/login.html', {'errors': errors, 'next': next})


def user_registration(request):
    firstname = request.POST.get('first_name', "")
    lastname = request.POST.get('last_name', "")
    username = request.POST.get('username', "")
    email = request.POST.get('email', "")
    password = request.POST.get('password', "")
    password_again = request.POST.get('password_again', "")
    if username == "":
        return render(request, 'backend/register.html')

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
    return HttpResponse("registration was successful")
