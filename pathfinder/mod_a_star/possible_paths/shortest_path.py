# imports
import os
import copy
import pickle



def get_connections_dict():
	# change directory
	os.chdir("../")
	os.chdir("possible_paths")
	# get shit from file
	f = open("rc_connections_dict.p", "rb")
	# load the pickle file
	connections_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("possible_paths")
	# return
	return connections_dict



def get_time_unit_connections_dict(connections_dict, weekday, time_unit):
	time_unit_connections_dict = connections_dict[weekday][time_unit]
	return time_unit_connections_dict



def start_journey(start_route_id, end_route_id, time_unit_connections_dict, been_list, journey_id_list):
	if start_route_id == end_route_id:
		return [True, {0: [start_route_id]}]
	# temp_dict
	temp_dict = dict()
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
		journey_id = 0
	# record that we've been to this bus stop
	been_list.append(start_route_id)
	# find the data we will use to start our journies
	list_of_route_ids = time_unit_connections_dict[start_route_id]
	# populate routes_dict
	for route_id in list_of_route_ids:
		# check if we've already been there
		if route_id not in been_list:
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			temp_dict[journey_id] = [start_route_id, route_id]
			# increment the journey_id
			journey_id += 1
	return [False, temp_dict]



def continue_journey(journey_id_list, journies_dict, been_list, end_route_id, time_unit_connections_dict):
	# sort journies so we know which is the shortest
	starting_dict = journies_dict
	# temp_dict that is the return object
	ending_dict = dict()
	# iterate over items in starting_dict
	for journey_id in starting_dict:
		# details
		path_details = starting_dict[journey_id]
		next_route_id = path_details[-1]
		# if the next_stop is our destination, then we have our route
		if next_route_id == end_route_id:
			ending_dict = dict()
			ending_dict[journey_id] = path_details
			return [True, ending_dict]
		# otherwise, we create the next set of possible paths
		else:
			# we get the information about the next possible routes
			next_list = time_unit_connections_dict[next_route_id]
			# iterate over possible next stops
			for next_route_id in next_list:
				if next_route_id not in been_list:
					# create a new journey id
					journey_id = journey_id_list[-1] + 1
					journey_id_list.append(journey_id)
					# populate ending_dict
					new_details = copy.deepcopy(path_details)
					new_details.append(next_route_id)
					ending_dict[journey_id] = new_details
	# return
	if not ending_dict:
		return [True, {0: None}]
	else:
		return [False, ending_dict]



def find_shortest_path(start_route_id, end_route_id, time_unit_connections_dict):
	# data objects
	found_shortest_path = False
	been_list = []
	journey_id_list = []
	journies_dict = dict()
	# start
	result = start_journey(start_route_id, end_route_id, time_unit_connections_dict, been_list, journey_id_list)
	journies_dict = result[1]
	found_shortest_path = result[0]
	# continue
	while found_shortest_path is False:
		result = continue_journey(journey_id_list, journies_dict, been_list, end_route_id, time_unit_connections_dict)
		found_shortest_path = result[0]
		journies_dict = result[1]
	# return
	return journies_dict



connections_dict = get_connections_dict()
time_unit_connections_dict = get_time_unit_connections_dict(connections_dict, 0, 7)
for start_route_id in time_unit_connections_dict:
	for end_route_id in time_unit_connections_dict:
		sp = find_shortest_path(start_route_id, end_route_id, time_unit_connections_dict)
		print(sp)