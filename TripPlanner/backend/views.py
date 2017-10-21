from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login


# Create your views here.
def index(request):
    return render(request, 'backend/index.html')


def user_login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/yay')
    else:
        return redirect('/nay')


def yay(request):
    html = "<html><body> Succesful login </body></html>"
    return HttpResponse(html)


def nay(request):
    html = "<html><body> Incorrect username, or password </body></html>"
    return HttpResponse(html)
