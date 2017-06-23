from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'), #calls index function, this is used for the 'homepage'
    url('selected_route', views.get_route, name='get_route'), #picking up selected route from the GET method, calling get_route function
]