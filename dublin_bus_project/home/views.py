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
import _3_stop_dijkstra as sd
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

        print(selected_origin,selected_destination,selected_day,selected_hour)
        """PATHFINDER START"""

        with open("stop_dict.p",'rb') as stop_dict_pkl:
            stop_dict=pkl.load(stop_dict_pkl)

        with open("r_dict.p","rb") as r_dict_pkl:
            r_dict = pkl.load(r_dict_pkl)

        sp = sd.the_shortest_path(stop_dict, r_dict, selected_day, selected_hour, selected_origin, selected_destination)

        print(sp)
        total_journey_time = int(round(sp[1][0]/60))
        print(total_journey_time)
        pathfinder_dict={}
        for route in sp[0]:
            pathfinder_dict[route]=[]

        for point_to_point in sp[1][1]:
            if point_to_point[0] not in pathfinder_dict[point_to_point[3]]:
                pathfinder_dict[point_to_point[3]].append(point_to_point[0])
            if point_to_point[1] not in pathfinder_dict[point_to_point[3]]:
                pathfinder_dict[point_to_point[3]].append(point_to_point[1])
        returned_stops=pathfinder_dict

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
        # print(journey_info)
        context = {'suggested_route':returned_stops,'returned_stops':returned_stops,'journey_time':total_journey_time,'journey_costs':journey_costs,'jpids_and_stops':stops_on_routes, 'stop_coordinates': stop_coordinates, 'weather_data':weather_data,'routes':routes}
        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))



#TIMETABLE LANDING PAGE
def timetable(request):
    print("timetable called")
    with open("home/stop_info.json") as stop_file:  # reading dictionary {key:value} = {stop:[lat,long]}
        stop_coordinates = json.load(stop_file)

    with open("home/jpids_and_stops.json") as jpids_and_stops:
        jpids_and_stops = json.load(jpids_and_stops)

    # # CHOSEN ROUTE DICT
    # with open("home/tt015B0001.json", 'r') as filename:
    #     for line in filename:
    #         tt_dict = json.loads(line)
    #
    #     tt_data = dict(
    #         jpid=tt_dict.get('jpid'),
    #         stops=tt_dict.get('stops'),
    #         weekday=tt_dict.get('Weekday'),
    #         sat=tt_dict.get('Sat'),
    #         sun=tt_dict.get('Sun')
    #     )

    context = {'jpids_and_stops': jpids_and_stops, 'stop_coordinates': stop_coordinates} #, 'tt_data':tt_data}
    template = loader.get_template('home/timetable.html')
    return HttpResponse(template.render(context, request))



#TIMETABLE RESULTS PAGE
def get_timetable(request):
        print("get_timetable called")
        with open("home/stop_info.json") as stop_file:  # reading dictionary {key:value} = {stop:[lat,long]}
            stop_coordinates = json.load(stop_file)

        with open("home/jpids_and_stops.json") as jpids_and_stops:
            jpids_and_stops = json.load(jpids_and_stops)

        # if request.method=="GET":
        #     routeNumberTT=int(request.GET.get('routeNumber'))
        # get_direction = "tt0" + str(routeNumberTT) + "0001"
        #
        # for key, value in jpids_and_stops.items():


        if request.method=="GET":
            routeNumberTT=str(request.GET.get('routeNumber'))

        # fileNum= "tt0" + str(routeNumberTT) + "0001"
        # print(fileNum)
        # path= "home/" + str(fileNum) + ".json"
        # CHOSEN ROUTE DICT
        #tt015B0001
        # route_dict={}
        # for file in glob.glob("home/timetable_results/tt015B")
        with open("home/timetable_results/tt015B0001.json", 'r') as filename:
            for line in filename:
                tt_dict = json.loads(line)

            tt_data = dict(
                jpid=tt_dict.get('jpid'),
                stops=tt_dict.get('stops'),
                weekday=tt_dict.get('Weekday'),
                sat=tt_dict.get('Sat'),
                sun=tt_dict.get('Sun')
                )
                # route_dict[]=tt_data

        context = {'jpids_and_stops': jpids_and_stops, 'stop_coordinates': stop_coordinates, 'tt_data': tt_data}
        template = loader.get_template('home/timetable.html')
        return HttpResponse(template.render(context, request))