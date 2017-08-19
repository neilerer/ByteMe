from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json
import pickle as pkl
import os
import pandas as pd
import urllib.request
import datetime
import _1_route_mapping as rm
import _3_route_connections as rc
import _4_shortest_paths as sp
import _5_pathfinder as pf

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

        selected_day=int(selected_day)

        if request.GET.get("hour"):
            selected_hour=request.GET.get("hour")
        else:
            selected_hour=str(datetime.datetime.now().time())
            selected_hour=int(selected_hour[:2])

        selected_hour=int(selected_hour)

        """PATHFINDER START"""
        with open("ctt_dict.p",'rb') as ctt_dict_pkl:
            ctt_dict=pkl.load(ctt_dict_pkl)

        with open("stop_dict.p",'rb') as stop_dict_pkl:
            stop_dict=pkl.load(stop_dict_pkl)

        r_dict = rm.routes_dict(stop_dict)

        grc_dict = rc.get_route_connections(stop_dict, ctt_dict, r_dict, selected_day, selected_hour, selected_origin, selected_destination)

        pp_dict = sp.possible_paths_dictionary(grc_dict, selected_origin, selected_destination)

        clean_pp_dict = sp.clean_possible_paths_dicitonary(pp_dict)

        pathfinder_dict = pf.pathfinder(clean_pp_dict, ctt_dict, selected_day, selected_hour)

        """PATHFINDER END"""

        #journey time calc
        for trip in pathfinder_dict:
            total_journey_time=float(trip)
            journey_info=pathfinder_dict[trip]
            break
        total_journey_time=int(round(total_journey_time)/60)

        print(journey_info)
        returned_stops={}
        for trip in journey_info:
            jpid=trip+"001"
            stops_on_jpid=stops_on_routes[jpid]
            print("ROUTE", jpid, stops_on_jpid)
            start_point=stops_on_jpid.index(str(journey_info[trip][0]))
            end_point=stops_on_jpid.index(str(journey_info[trip][1]))

            returned_stops[jpid]=stops_on_jpid[start_point:end_point+1]

        print(returned_stops)

        """JOURNEY COST START"""

        with open("home/dublin_bus_fares.json") as price_file:
            prices = json.load(price_file)
        leap_fares = prices['leap_fares']
        cash_fares = prices['cash_fares']
        journey_cost_leap,journey_cost_cash=0,0
        for key in returned_stops:
            if len(returned_stops[key])-1<4:
                journey_cost_leap+=leap_fares[0]
                journey_cost_cash+=cash_fares[0]
            elif len(returned_stops[key])-1<14:
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

        context = {'suggested_route':journey_info,'returned_stops':returned_stops,'journey_time':total_journey_time,'journey_costs':journey_costs,'jpids_and_stops':stops_on_routes, 'stop_coordinates': stop_coordinates, 'weather_data':weather_data,'routes':routes}
        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

