# imports
import os
import pickle



def get_model_data():
	# change directory
	os.chdir("../")
	os.chdir("data_json")
	# get shit from file
	f = open("data.p", "rb")
	# load the pickle file
	model_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("pathfinder_possible_paths")
	# return
	return model_dict


# break these into weekdays, time_units, and then stops

def routes_at_stop(stop, stop_linked_list):
	stop_data = stop_linked_list[stop]
	route_list = list()
	for quadruple in stop_data:
		route = quadruple[1]
		route_list.append(route)
	return route_list

def route_connections(stop_linked_list):
	rc_dict = dict()
	for stop in stop_linked_list:
		connected_stops = routes_at_stop(stop, stop_linked_list)
		for cs in connected_stops:
			if cs not in rc_dict:
				rc_dict[cs] = list()
			for other_cs in connected_stops:
				if other_cs != cs and other_cs not in rc_dict[cs]:
					rc_dict[cs].append(other_cs)
	return rc_dict