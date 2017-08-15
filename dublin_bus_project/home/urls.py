from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'), #calls index function, this is used for the 'homepage'
    url('route_selection', views.get_route, name='get_route'), #picking up selected route from the GET method, calling get_route function
    url('timetable', views.get_timetable, name='timetable') #take selected route with GET, return timetable
]