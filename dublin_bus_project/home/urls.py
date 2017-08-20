from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'), #calls index function, this is used for the 'homepage'
]