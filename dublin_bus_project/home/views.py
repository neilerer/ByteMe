from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json


def index(request): #called from home urls.py file
    routes=['15', '46A', '14', '41B', '39A', '65', '40D', '11', '31', '27', '67', '79', '42', '66A', '33B', '140', '44', '83A', '27B', '38', '16C', '747', '41C', '39', '25', '239', '43', '70', '13', '150', '145', '77A', '184', '84', '61', '83', '40', '66', '15A', '123', '17A', '16', '14C', '9', '4', '37', '32', '33', '49', '56A', '151', '25A', '45A', '54A', '47', '18', '7', '17', '102', '120', '65B', '41', '122', '29A', '76', '68', '59', '25B', '69', '27A', '66B', '38B', '7D', '75', '15B', '84A', '63', '84X', '33X', '68A', '1', '76A', '7B', '270', '236', '130', '238', '220', '44B', '40B', '26', '32B', '8', '41A', '53', '67X', '104', '32A', '79A', '114', '185', '66X', '31B', '32X', '51X', '51D', '41X', '142', '111', '69X', '27X', '116', '46E', '161', '118', '25X', '38A', '33A', '31A']
    context={'routes':routes} #homepage requires only the routes for the dropdown menu
    template = loader.get_template('home/index.html')  # loading the html homepage
    return HttpResponse(template.render(context, request)) #rendering routes to index.html

def get_route(request):
    if request.method=='GET':
        selected_route = request.GET.get('selected_route') # name of select field (line 18 index.html) used to pick up form value
        routes = ['15', '46A', '14', '41B', '39A', '65', '40D', '11', '31', '27', '67', '79', '42', '66A', '33B',
                  '140', '44', '83A', '27B', '38', '16C', '747', '41C', '39', '25', '239', '43', '70', '13', '150',
                  '145', '77A', '184', '84', '61', '83', '40', '66', '15A', '123', '17A', '16', '14C', '9', '4',
                  '37', '32', '33', '49', '56A', '151', '25A', '45A', '54A', '47', '18', '7', '17', '102', '120',
                  '65B', '41', '122', '29A', '76', '68', '59', '25B', '69', '27A', '66B', '38B', '7D', '75', '15B',
                  '84A', '63', '84X', '33X', '68A', '1', '76A', '7B', '270', '236', '130', '238', '220', '44B',
                  '40B', '26', '32B', '8', '41A', '53', '67X', '104', '32A', '79A', '114', '185', '66X', '31B',
                  '32X', '51X', '51D', '41X', '142', '111', '69X', '27X', '116', '46E', '161', '118', '25X', '38A',
                  '33A', '31A']
        with open("home/stops_on_routes.json") as route_file: #reading dictionary {key:value} = {stop:[routes]}
            stops_on_routes = json.load(route_file)
        with open("home/stop_coordinates.json") as stop_file: #reading dictionary {key:value} = {stop:[lat,long]}
            stop_coordinates = json.load(stop_file)
        context = {'stops_on_routes': stops_on_routes[selected_route], 'routes': routes, 'stop_coordinates': stop_coordinates, 'selected_route':selected_route}
        #renders stops relating to selected route, the route list, coordinates of all stops, and the selected route to index.html
        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

