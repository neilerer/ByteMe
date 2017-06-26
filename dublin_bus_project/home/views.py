from django.http import HttpResponse
from django.template import loader
from django.shortcuts import render
import json


def index(request): #called from home urls.py file
    routes=['102y', '102z', '104y', '104z', '111y', '111z', '114y', '114z', '116y', '116z', '118y', '11y', '11z', '120y', '120z', '122y', '122z', '123y', '123z', '130y', '130z', '13y', '13z', '140y', '140z', '142y', '142z', '145y', '145z', '14Cy', '14Cz', '14y', '14z', '150y', '150z', '151y', '151z', '15Ay', '15Az', '15By', '15Bz', '15y', '15z', '161y', '161z', '16Cy', '16Cz', '16y', '16z', '17Ay', '17Az', '17y', '17z', '184y', '184z', '185y', '185z', '18y', '18z', '1y', '1z', '220y', '220z', '236y', '236z', '238y', '238z', '239y', '239z', '25Ay', '25Az', '25By', '25Bz', '25Xy', '25Xz', '25y', '25z', '26y', '26z', '270y', '270z', '27Ay', '27Az', '27By', '27Bz', '27Xy', '27Xz', '27y', '27z', '29Ay', '29Az', '31Ay', '31Az', '31By', '31Bz', '31y', '31z', '32Ay', '32Az', '32By', '32Bz', '32Xy', '32Xz', '32y', '32z', '33Ay', '33Az', '33By', '33Bz', '33Xy', '33Xz', '33y', '33z', '37y', '37z', '38Ay', '38Az', '38By', '38Bz', '38y', '38z', '39Ay', '39Az', '39y', '39z', '40By', '40Bz', '40Dy', '40Dz', '40y', '40z', '41Ay', '41By', '41Bz', '41Cy', '41Cz', '41Xy', '41Xz', '41y', '41z', '42y', '42z', '43y', '43z', '44By', '44Bz', '44y', '44z', '45Ay', '45Az', '46Ay', '46Az', '46Ey', '47y', '47z', '49y', '49z', '4y', '4z', '51Dy', '51Dz', '51Xy', '53By', '53Bz', '53y', '53z', '54Ay', '54Az', '56Ay', '56Az', '59y', '59z', '61y', '61z', '63y', '63z', '65By', '65Bz', '65y', '65z', '66Ay', '66Az', '66By', '66Bz', '66Xy', '66Xz', '66y', '66z', '67Xy', '67Xz', '67y', '67z', '68Ay', '68Az', '68y', '68z', '69Xy', '69Xz', '69y', '69z', '70y', '70z', '747y', '747z', '75y', '75z', '76Ay', '76Az', '76y', '76z', '77Ay', '77Az', '79Ay', '79Az', '79y', '79z', '7By', '7Bz', '7Dy', '7Dz', '7y', '7z', '83Ay', '83Az', '83y', '83z', '84Ay', '84Az', '84Xy', '84Xz', '84y', '84z', '8y', '8z', '9y', '9z']
    context={'routes':routes} #homepage requires only the routes for the dropdown menu
    template = loader.get_template('home/index.html')  # loading the html homepage
    return HttpResponse(template.render(context, request)) #rendering routes to index.html

def get_route(request):
    if request.method=='GET':
        selected_route = request.GET.get('selected_route') # name of select field (line 18 index.html) used to pick up form value
        print(selected_route)
        # routes = ['15', '46A', '14', '41B', '39A', '65', '40D', '11', '31', '27', '67', '79', '42', '66A', '33B',
        #           '140', '44', '83A', '27B', '38', '16C', '747', '41C', '39', '25', '239', '43', '70', '13', '150',
        #           '145', '77A', '184', '84', '61', '83', '40', '66', '15A', '123', '17A', '16', '14C', '9', '4',
        #           '37', '32', '33', '49', '56A', '151', '25A', '45A', '54A', '47', '18', '7', '17', '102', '120',
        #           '65B', '41', '122', '29A', '76', '68', '59', '25B', '69', '27A', '66B', '38B', '7D', '75', '15B',
        #           '84A', '63', '84X', '33X', '68A', '1', '76A', '7B', '270', '236', '130', '238', '220', '44B',
        #           '40B', '26', '32B', '8', '41A', '53', '67X', '104', '32A', '79A', '114', '185', '66X', '31B',
        #           '32X', '51X', '51D', '41X', '142', '111', '69X', '27X', '116', '46E', '161', '118', '25X', '38A',
        #           '33A', '31A']
        routes=['102y', '102z', '104y', '104z', '111y', '111z', '114y', '114z', '116y', '116z', '118y', '11y', '11z', '120y', '120z', '122y', '122z', '123y', '123z', '130y', '130z', '13y', '13z', '140y', '140z', '142y', '142z', '145y', '145z', '14Cy', '14Cz', '14y', '14z', '150y', '150z', '151y', '151z', '15Ay', '15Az', '15By', '15Bz', '15y', '15z', '161y', '161z', '16Cy', '16Cz', '16y', '16z', '17Ay', '17Az', '17y', '17z', '184y', '184z', '185y', '185z', '18y', '18z', '1y', '1z', '220y', '220z', '236y', '236z', '238y', '238z', '239y', '239z', '25Ay', '25Az', '25By', '25Bz', '25Xy', '25Xz', '25y', '25z', '26y', '26z', '270y', '270z', '27Ay', '27Az', '27By', '27Bz', '27Xy', '27Xz', '27y', '27z', '29Ay', '29Az', '31Ay', '31Az', '31By', '31Bz', '31y', '31z', '32Ay', '32Az', '32By', '32Bz', '32Xy', '32Xz', '32y', '32z', '33Ay', '33Az', '33By', '33Bz', '33Xy', '33Xz', '33y', '33z', '37y', '37z', '38Ay', '38Az', '38By', '38Bz', '38y', '38z', '39Ay', '39Az', '39y', '39z', '40By', '40Bz', '40Dy', '40Dz', '40y', '40z', '41Ay', '41By', '41Bz', '41Cy', '41Cz', '41Xy', '41Xz', '41y', '41z', '42y', '42z', '43y', '43z', '44By', '44Bz', '44y', '44z', '45Ay', '45Az', '46Ay', '46Az', '46Ey', '47y', '47z', '49y', '49z', '4y', '4z', '51Dy', '51Dz', '51Xy', '53By', '53Bz', '53y', '53z', '54Ay', '54Az', '56Ay', '56Az', '59y', '59z', '61y', '61z', '63y', '63z', '65By', '65Bz', '65y', '65z', '66Ay', '66Az', '66By', '66Bz', '66Xy', '66Xz', '66y', '66z', '67Xy', '67Xz', '67y', '67z', '68Ay', '68Az', '68y', '68z', '69Xy', '69Xz', '69y', '69z', '70y', '70z', '747y', '747z', '75y', '75z', '76Ay', '76Az', '76y', '76z', '77Ay', '77Az', '79Ay', '79Az', '79y', '79z', '7By', '7Bz', '7Dy', '7Dz', '7y', '7z', '83Ay', '83Az', '83y', '83z', '84Ay', '84Az', '84Xy', '84Xz', '84y', '84z', '8y', '8z', '9y', '9z']
        # with open("home/stops_on_routes.json") as route_file: #reading dictionary {key:value} = {stop:[routes]}
        #     stops_on_routes = json.load(route_file)
        with open("home/route_stops_with_directions.json") as route_file: #reading dictionary {key:value} = {stop:[routes]}
            stops_on_routes = json.load(route_file)
        with open("home/stop_coordinates.json") as stop_file: #reading dictionary {key:value} = {stop:[lat,long]}
            stop_coordinates = json.load(stop_file)
        context = {'stops_on_routes': stops_on_routes[selected_route], 'routes': routes, 'stop_coordinates': stop_coordinates, 'selected_route':selected_route}
        #renders stops relating to selected route, the route list, coordinates of all stops, and the selected route to index.html
        template = loader.get_template('home/index.html')
        return HttpResponse(template.render(context, request))

