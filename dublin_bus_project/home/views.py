from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
import pickle as pkl
import os
import pandas as pd
import urllib.request
import pathfinder
import minimum_transfers
import datetime
from math import sin, cos, sqrt, atan2, radians

def index(request): #called from home urls.py file

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

    # loading in json data
    with open("home/jpids_and_stops.json") as route_file:  # reading dictionary {key:value} = {stop:[routes]}
        stops_on_routes = json.load(route_file)
    with open("home/stop_info.json") as stop_file:  # reading dictionary {key:value} = {stop:[lat,long]}
        stop_coordinates = json.load(stop_file)
    with open("../models/linear_model/route_list", "rb") as route_file:  # loading pickle file with routes
        routes = pkl.load(route_file)
        routes=sorted(routes)


    # getting selected form values
    if request.method=="GET":
        selected_origin=int(request.GET.get('origin'))
        selected_destination=int(request.GET.get('destination'))

        #if no day/time selected, current values used
        if request.GET.get("day"):
            selected_day=request.GET.get("day")
        else:
            selected_day=datetime.date.today().weekday()

        if request.GET.get("hour"):
            selected_hour=request.GET.get("hour")
        else:
            selected_hour=str(datetime.datetime.now().time())
            selected_hour=int(selected_hour[:2])

        """PATHFINDER START"""
        with open("data.p", 'rb') as data_pkl:
            # results from every model input
            pathfinder_data = pkl.load(data_pkl)

        pathfinder_output=[]
        min_time=99999999999
        best_journey=0
        for close_to_origin in stop_coordinates[str(selected_origin)][4]: # closest stops to origin
            close_to_origin=int(close_to_origin)
            for close_to_destination in stop_coordinates[str(selected_destination)][4]:
                close_to_destination=int(close_to_destination)
                try:
                    shortest_path_raw = pathfinder.pathfinder(selected_day, selected_hour, close_to_origin, close_to_destination, pathfinder_data)
                    destination_route_list = minimum_transfers.destination_routes(close_to_destination, selected_day, selected_hour, pathfinder_data)
                    min_tran = minimum_transfers.minimum_transfers(shortest_path_raw, destination_route_list, close_to_origin, close_to_destination, selected_day, selected_hour,pathfinder_data)
                    print("min_tran done")
                    new_pathfinder_output=minimum_transfers.output_for_django(min_tran)
                    total_journey_time = 0
                    for trip in new_pathfinder_output:
                        total_journey_time += new_pathfinder_output[trip][0]
                    if best_journey==0:
                        best_journey=new_pathfinder_output
                    if total_journey_time<min_time:
                        min_time=total_journey_time
                        best_journey=new_pathfinder_output
                    print("new_pathfinder done")
                    pathfinder_output.append(new_pathfinder_output)
                except:
                    continue
        print(min_time)
        print(best_journey)

        """PATHFINDER END"""

        # #journey time calc
        # total_journey_time=0
        # for trip in pathfinder_output:
        #     total_journey_time+=pathfinder_output[trip][0]

        total_journey_time=int(round(min_time)/60)

        """JOURNEY COST START"""
        leap_fares = [1.50, 2.05, 2.60]
        cash_fares = [2.00, 2.70, 3.30]
        journey_cost_leap,journey_cost_cash=0,0
        for key in pathfinder_output:
            if len(pathfinder_output[key][1])-1<4:
                journey_cost_leap+=leap_fares[0]
                journey_cost_cash+=cash_fares[0]
            elif len(pathfinder_output[key][1])-1<14:
                journey_cost_leap += leap_fares[1]
                journey_cost_cash += cash_fares[1]
            else:
                journey_cost_leap += leap_fares[2]
                journey_cost_cash += cash_fares[2]
        journey_cost_leap,journey_cost_cash='{0:.2f}'.format(journey_cost_leap),'{0:.2f}'.format(journey_cost_cash)
        journey_costs={'leap':journey_cost_leap,'cash':journey_cost_cash}
        """JOURNEY COST END"""

        """APIS START"""
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
        """APIS END"""

        context = {'suggested_route':pathfinder_output,'journey_time':total_journey_time,'journey_costs':journey_costs,'jpids_and_stops':stops_on_routes, 'stop_coordinates': stop_coordinates, 'weather_data':weather_data,'routes':routes}
        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

