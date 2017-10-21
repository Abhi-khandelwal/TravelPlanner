from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login', views.user_login, name='login'),
    url(r'^yay', views.yay, name='yay'),
    url(r'^nay', views.nay, name='nay'),
    url(r'^hidden', views.hidden, name='hidden'),
    url(r'^', views.index, name='index'),
]
