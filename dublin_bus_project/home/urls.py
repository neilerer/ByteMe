from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'), #calls index function, this is used for the 'homepage'
    url('select_journey', views.get_route, name='get_route'), #picking up selected route from the GET method, calling get_route function
    url('timetable', views.timetable, name='timetable'),  # render timetable template, with query form
    url('select_ttable', views.get_timetable, name='select_timetable'),  # render timetable results, with query form
]