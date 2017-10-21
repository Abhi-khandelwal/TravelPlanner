from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .models import Trip


# Create your views here.
def index(request):
    return render(request, 'backend/index.html')


@login_required(login_url='/admin/login/')
def dashboard(request):
    trips = [trip.get_data() for trip in Trip.get_trips_of_user(request.user)]
    return render(request, 'backend/dashboard.html', {'trips': trips})


def user_login(request):
    username = request.POST.get('username', "")
    password = request.POST.get('password', "")
    if username == "":
        return render(request, 'backend/login.html')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('yay')
    else:
        return redirect('nay')


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



@login_required
def hidden(request):
    return HttpResponse("hidden")


def yay(request):
    html = "<html><body> Successful login </body></html>"
    return HttpResponse(html)


def nay(request):
    html = "<html><body> Incorrect username, or password </body></html>"
    return HttpResponse(html)
