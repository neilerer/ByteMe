from django.conf.urls import url
from . import views

urlpatterns=[
    url(r'^$', views.index, name='index'), #calls index function, this is used for the 'homepage'
    url('timetable', views.timetable, name='timetable'),  # render timetable template, with query form
    url('select_timetable', views.get_timetable, name='get_timetable'),  # render timetable results, with query form
]