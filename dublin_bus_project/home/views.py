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

        """PATHFINDER START"""

        with open("stop_dict.p",'rb') as stop_dict_pkl:
            stop_dict=pkl.load(stop_dict_pkl)

        r_dict = rm.routes_dict(stop_dict)
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
        print(returned_stops)
        # possibilities=[pathfinder_dict]
        #
        # print(possibilities)

        # come back to this loop - not working
        # possibilities=[]
        # for near_origin in stop_coordinates[str(selected_origin)][4]:
        #     for near_destination in stop_coordinates[str(selected_destination)][4]:
        #
        #         r_dict=rm.routes_dict(stop_dict)
        #
        #         grc_dict = rc.get_route_connections(stop_dict, ctt_dict, r_dict, selected_day, selected_hour, near_origin, near_destination)
        #
        #         pp_dict = sp.possible_paths_dictionary(grc_dict, near_origin, near_destination)
        #
        #         clean_pp_dict = sp.clean_possible_paths_dicitonary(pp_dict)
        #
        #         pathfinder_dict = pf.pathfinder(clean_pp_dict, ctt_dict, selected_day, selected_hour)
        #
        #         possibilities.append(pathfinder_dict)
        #
        # print(possibilities)
        """PATHFINDER END"""

        # """PATHFINDER START"""
        # with open("data.p", 'rb') as data_pkl:
        #     # results from every model input
        #     pathfinder_data = pkl.load(data_pkl)
        #
        # pathfinder_output=[]
        # min_time=99999999999
        # best_journey=0
        # for close_to_origin in stop_coordinates[str(selected_origin)][4]: # closest stops to origin
        #     close_to_origin=int(close_to_origin)
        #     for close_to_destination in stop_coordinates[str(selected_destination)][4]:
        #         close_to_destination=int(close_to_destination)
        #         try:
        #             shortest_path_raw = pathfinder.pathfinder(selected_day, selected_hour, close_to_origin, close_to_destination, pathfinder_data)
        #             destination_route_list = minimum_transfers.destination_routes(close_to_destination, selected_day, selected_hour, pathfinder_data)
        #             min_tran = minimum_transfers.minimum_transfers(shortest_path_raw, destination_route_list, close_to_origin, close_to_destination, selected_day, selected_hour,pathfinder_data)
        #             print("min_tran done")
        #             new_pathfinder_output=minimum_transfers.output_for_django(min_tran)
        #             total_journey_time = 0
        #             for trip in new_pathfinder_output:
        #                 total_journey_time += new_pathfinder_output[trip][0]
        #             if best_journey==0:
        #                 best_journey=new_pathfinder_output
        #             if total_journey_time<min_time:
        #                 min_time=total_journey_time
        #                 best_journey=new_pathfinder_output
        #             print("new_pathfinder done")
        #             pathfinder_output.append(new_pathfinder_output)
        #         except:
        #             continue
        # print(min_time)
        # print(best_journey)
        #
        # """PATHFINDER END"""

        # #journey time calc

        # returned_stops={}
        # for trip in journey_info:
        #     jpid=trip+"001"
        #     stops_on_jpid=stops_on_routes[jpid]
        #     start_point=stops_on_jpid.index(str(journey_info[trip][0]))
        #     end_point=stops_on_jpid.index(str(journey_info[trip][1]))
        #     returned_stops[jpid]=stops_on_jpid[start_point:end_point+1]

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

    with open("home/stop_info.json") as stop_file:  # reading dictionary {key:value} = {stop:[lat,long]}
        stop_coordinates = json.load(stop_file)

    with open("home/jpids_and_stops.json") as jpids_and_stops:
        jpids_and_stops = json.load(jpids_and_stops)

    # CHOSEN ROUTE DICT
    with open("home/tt015B0001.json", 'r') as filename:
        for line in filename:
            tt_dict = json.loads(line)

        tt_data = dict(
            jpid=tt_dict.get('jpid'),
            stops=tt_dict.get('stops'),
            weekday=tt_dict.get('Weekday'),
            sat=tt_dict.get('Sat'),
            sun=tt_dict.get('Sun')
        )

    context = {'jpids_and_stops': jpids_and_stops, 'stop_coordinates': stop_coordinates} #, 'tt_data':tt_data}
    template = loader.get_template('home/timetable.html')
    return HttpResponse(template.render(context, request))


#TIMETABLE RESULTS PAGE
def get_timetable(request):

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

    fileNum= "tt0" + str(routeNumberTT) + "0001"
    print(fileNum)
    path= "home/" + str(fileNum) + ".json"
    # CHOSEN ROUTE DICT
    #tt015B0001
    with open(path, 'r') as filename:
        for line in filename:
            tt_dict = json.loads(line)

        tt_data = dict(
            jpid=tt_dict.get('jpid'),
            stops=tt_dict.get('stops'),
            weekday=tt_dict.get('Weekday'),
            sat=tt_dict.get('Sat'),
            sun=tt_dict.get('Sun')
        )

    #OTHER DIRECTION
    fileNum = "tt0" + str(routeNumberTT) + "1001"
    print(fileNum)
    path = "home/" + str(fileNum) + ".json"
    # CHOSEN ROUTE DICT
    # tt015B0001
    with open(path, 'r') as filename:
        for line in filename:
            tt_dict2 = json.loads(line)

        tt_data2 = dict(
            jpid=tt_dict.get('jpid'),
            stops=tt_dict.get('stops'),
            weekday=tt_dict.get('Weekday'),
            sat=tt_dict.get('Sat'),
            sun=tt_dict.get('Sun')
        )

    context = {'jpids_and_stops': jpids_and_stops, 'stop_coordinates': stop_coordinates, 'tt_data': tt_data, 'tt_data2': tt_data2}
    template = loader.get_template('home/timetable.html')
    return HttpResponse(template.render(context, request))
