from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^login', views.login, name='login'),
    url(r'^yay', views.yay, name='yay'),
    url(r'^nay', views.nay, name='nay'),
    url(r'^', views.index, name='index'),
]
