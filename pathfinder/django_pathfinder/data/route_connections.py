# imports
import os
import pickle



# GET DATA
def get_model_data():
	# get shit from file
	f = open("data2.p", "rb")
	# load the pickle file
	model_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# return
	return model_dict



# ROUTES
def routes_at_stop(stop, time_unit_data):
	stop_data = time_unit_data[stop]
	route_list = list()
	for quadruple in stop_data:
		route = quadruple[3]
		if route not in route_list:
			route_list.append(route)
	return route_list

def routes_in_time_unit(time_unit, weekday_data):
	routes_in_time_unit_dict = dict()
	time_unit_data = weekday_data[time_unit]
	for stop in time_unit_data:
		routes_in_time_unit_dict[stop] = routes_at_stop(stop, time_unit_data)
	return routes_in_time_unit_dict

def routes_in_weekday(weekday, model_dict):
	routes_in_weekday_dict = dict()
	weekday_data = model_dict[weekday]
	for time_unit in weekday_data:
		routes_in_weekday_dict[time_unit] = routes_in_time_unit(time_unit, weekday_data)
	return routes_in_weekday_dict

def routes(model_dict):
	routes_dict = dict()
	for weekday in model_dict:
		routes_dict[weekday] = routes_in_weekday(weekday, model_dict)
	return routes_dict



# ROUTE CONNECTIONS
def connections_in_time_unit(time_unit, weekday_data):
	connections_in_time_unit_dict = dict()
	routes_in_time_unit_dict = routes_in_time_unit(time_unit, weekday_data)
	for stop in routes_in_time_unit_dict:
		connected_stops = routes_in_time_unit_dict[stop]
		for cs in connected_stops:
			if cs not in connections_in_time_unit_dict:
				connections_in_time_unit_dict[cs] = list()
			for other_cs in connected_stops:
				if (other_cs != cs) and (other_cs not in connections_in_time_unit_dict[cs]):
					connections_in_time_unit_dict[cs].append(other_cs)
	return connections_in_time_unit_dict

def connections_in_weekday(weekday, model_dict):
	connections_in_weekday_dict = dict()
	weekday_data = model_dict[weekday]
	for time_unit in weekday_data:
		connections_in_weekday_dict[time_unit] = connections_in_time_unit(time_unit, weekday_data)
	return connections_in_weekday_dict

def connections(model_dict):
	connections_dict = dict()
	for weekday in model_dict:
		connections_dict[weekday] = connections_in_weekday(weekday, model_dict)
	return connections_dict


# TO FILE
def routes_to_file():
	model_dict = get_model_data()
	routes_dict = routes(model_dict)
	destination = open("rc_routes_dict2.p", "wb")
	# dump the data into the pickle file
	pickle.dump(routes_dict, destination)
	# close the file
	destination.close()

def connections_to_file():
	model_dict = get_model_data()
	connections_dict = connections(model_dict)
	destination = open("rc_connections_dict2.p", "wb")
	# dump the data into the pickle file
	pickle.dump(connections_dict, destination)
	# close the file
	destination.close()



if __name__ == "__main__":
	# routes_to_file()
	connections_to_file()