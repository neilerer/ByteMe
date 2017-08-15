from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
import pickle as pkl
import os
import pandas as pd
import urllib.request
import pathfinder
import pathfinder_django

def index(request): #called from home urls.py file


    # """PATHFINDER START"""
    #
    # with open("data.p",'rb') as data_pkl:
    #     # results from every model input
    #     pathfinder_data=pkl.load(data_pkl)
    # with open("rc_connections_dict.p", 'rb') as connections_pkl:
    #     # shortest path via routes start to end
    #     pathfinder_connections=pkl.load(connections_pkl)
    #
    # wd_list=pathfinder_django.weekday_list()
    # tu_list=pathfinder_django.time_unit_list(wd_list)
    # si_dict=pathfinder_django.stop_id_dict()
    #
    # shortest_path_raw=pathfinder.pathfinder(3,17,400,4486,pathfinder_data,pathfinder_connections)
    #
    # print(pathfinder_django.pathfinder_for_django(shortest_path_raw))
    #
    # """PATHFINDER END"""


    # hardcoded list of currently available routes, needs to be generated for all routes later
    with open("../models/linear_model/route_list", "rb") as route_file:  # loading pickle file with routes
        routes = pkl.load(route_file)
        routes=sorted(routes)

    with open("home/stop_info.json") as stop_file:  # reading dictionary {key:value} = {stop:[lat,long]}
        stop_coordinates = json.load(stop_file)

    with open("home/jpids_and_stops.json") as jpids_and_stops:
        jpids_and_stops= json.load(jpids_and_stops)

    url = 'http://api.wunderground.com/api/'

    wu_key = 'fc74b20ed4eafd0b'
    lat = "53.355122"
    lon = "-6.24922"
    final_url = url + wu_key + "/geolookup/conditions/q/" + lat + "," + lon + ".json"
    url_open = urllib.request.urlopen(final_url)
    json_string = url_open.read()
    parsed_json = json.loads(json_string)
    url_open.close()

    weather_data = dict(
        location=parsed_json.get('location').get('city'),
        temp_c=parsed_json.get('current_observation').get('temp_c'),
        weather=parsed_json.get('current_observation').get('weather'),
        pressure=parsed_json.get('current_observation').get('pressure_mb'),
        wind=parsed_json.get('current_observation').get('wind_kph'),
        iconURL=parsed_json.get('current_observation').get('icon_url'),
        icon=parsed_json.get('current_observation').get('icon')
    )

    context={'routes':routes, 'jpids_and_stops':jpids_and_stops,'stop_coordinates':stop_coordinates, 'weather_data':weather_data} #homepage requires only the routes for the dropdown menu
    template = loader.get_template('home/index.html')  # loading the html homepage
    return HttpResponse(template.render(context, request)) #rendering routes to index.html

def get_route(request):
    routes=sorted(['39A','46A','77A','4','41','7','9','14','15','27','40','83','122','123','140','145'])
    if request.method=='GET': # getting form submission values from index.html
        selected_route=request.GET.get('route')
        selected_direction=request.GET.get('direction')
        selected_start=request.GET.get('start')
        selected_end = request.GET.get('end')
        selected_day = request.GET.get('weekday')
        selected_hour = request.GET.get('hour')

        for i in range(4-len(selected_route)):
            selected_route="0"+str(selected_route)
        selected_route+=str(selected_direction)+"001"

        with open("home/jpids_and_stops.json") as route_file: #reading dictionary {key:value} = {stop:[routes]}
            stops_on_routes = json.load(route_file)
        with open("home/stop_info.json") as stop_file: #reading dictionary {key:value} = {stop:[lat,long]}
            stop_coordinates = json.load(stop_file)
        print(os.getcwd())
        with open("../models/linear_model/pickle_files/"+selected_route+".pkl", "rb") as model_file:
            model = pkl.load(model_file)

            end_predict_dict={'StopSeq':[selected_end],'WeekDay':[selected_day],'Hours':[selected_hour]}
            end_predict_df=pd.DataFrame.from_dict(end_predict_dict)
            end_predict_df=end_predict_df[['StopSeq','WeekDay','Hours']]
            end_ctt=model.predict(end_predict_df)[0]

            if int(selected_start)==0:
                start_ctt=0
            else:
                start_predict_dict = {'StopSeq': [selected_start], 'WeekDay': [selected_day], 'Hours': [selected_hour]}
                start_predict_df = pd.DataFrame.from_dict(start_predict_dict)
                start_predict_df = start_predict_df[['StopSeq', 'WeekDay', 'Hours']]
                start_ctt = model.predict(start_predict_df)[0]

            result=int(round((end_ctt-start_ctt)//60))

            returned_stops=stops_on_routes[selected_route][int(selected_start):int(selected_end)+1]

        url = 'http://api.wunderground.com/api/'

        wu_key = 'fc74b20ed4eafd0b'
        lat = "53.355122"
        lon = "-6.24922"
        final_url = url + wu_key + "/geolookup/conditions/q/" + lat + "," + lon + ".json"
        url_open = urllib.request.urlopen(final_url)
        json_string = url_open.read()
        parsed_json = json.loads(json_string)
        url_open.close()

        weather_data = dict(
            location=parsed_json.get('location').get('city'),
            temp_c=parsed_json.get('current_observation').get('temp_c'),
            weather=parsed_json.get('current_observation').get('weather'),
            pressure=parsed_json.get('current_observation').get('pressure_mb'),
            wind=parsed_json.get('current_observation').get('wind_kph'),
            iconURL=parsed_json.get('current_observation').get('icon_url'),
            icon=parsed_json.get('current_observation').get('icon')
        )

        context = {'routes':routes,'jpids_and_stops':stops_on_routes,'stops_on_routes': returned_stops, 'trip_length':len(returned_stops)-1, 'stop_coordinates': stop_coordinates, 'estimated_time':result, 'current_route':selected_route, 'start_point':selected_start, 'end_point':selected_end, 'weather_data':weather_data}
        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

def get_timetable(request): #request
    with open('home/results/tt017A0001.txt', 'r') as output:
        tt_file = json.load(output)

    context = []
    template = loader.get_template('home/timetable.html')
    return HttpResponse(template.render(context, response)
    #return HttpResponse("<h2>HEY!</h2>")
