from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    return render(request, 'backend/index.html')


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


@login_required
def hidden(request):
    return HttpResponse("hidden")


def yay(request):
    html = "<html><body> Successful login </body></html>"
    return HttpResponse(html)


def nay(request):
    html = "<html><body> Incorrect username, or password </body></html>"
    return HttpResponse(html)
