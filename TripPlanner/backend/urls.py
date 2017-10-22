from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^register', views.user_registration, name='register'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
    url(r'^dashboard', views.dashboard, name='dashboard'),
    url(r'^addtrip', views.create_trip, name='addtrip'),
    url(r'^', views.index, name='index'),
]
