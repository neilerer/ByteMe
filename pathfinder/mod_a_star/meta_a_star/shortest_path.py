# imports
import copy
import merge_sort


def get_time_unit_connections_dict(connections_dict, weekday, time_unit):
	time_unit_connections_dict = connections_dict[weekday][time_unit]
	return time_unit_connections_dict



# def start_journey(start_route_id, end_route_id, time_unit_connections_dict, been_list, journey_id_list):
# 	if start_route_id == end_route_id:
# 		return [True, {0: [start_route_id]}]
# 	# temp_dict
# 	temp_dict = dict()
# 	# instantiate journey_id
# 	try:
# 		journey_id = journey_id_list[-1] + 1
# 	except:
# 		journey_id = 0
# 	# record that we've been to this bus stop
# 	been_list.append(start_route_id)
# 	# find the data we will use to start our journies
# 	list_of_route_ids = time_unit_connections_dict[start_route_id]
# 	# populate routes_dict
# 	for route_id in list_of_route_ids:
# 		# check if we've already been there
# 		if route_id not in been_list:
# 			# record the journey_id
# 			journey_id_list.append(journey_id)
# 			# create the journey details
# 			temp_dict[journey_id] = [start_route_id, route_id]
# 			# increment the journey_id
# 			journey_id += 1
# 	return [False, temp_dict]



def start_journey(start_route_id, end_route_id, time_unit_connections_dict, journey_id_list):
	if start_route_id == end_route_id:
		return [True, {0: [None, [start_route_id]]}]
	# temp_dict
	ending_dict = dict()
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
		journey_id = 0
	# record that we've been to this bus stop
	been_set = {start_route_id}
	# find the data we will use to start our journies
	list_of_route_ids = time_unit_connections_dict[start_route_id]
	# populate routes_dict
	for route_id in list_of_route_ids:
		# check if we've already been there
		if route_id not in been_set:
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			ending_dict[journey_id] = [been_set, [start_route_id, route_id]]
			# increment the journey_id
			journey_id += 1
	return [False, ending_dict]

def continue_journey(journey_id_list, journies_dict, end_route_id, time_unit_connections_dict):
	# sort journies so we know which is the shortest
	continuing_dict = journies_dict
	# sort continuing_dict by length of route
	continuing_dict = merge_sort.merge_sort_path_dict(continuing_dict)
	# continue the shortest path
	current_path_details = merge_sort.remove_first_entry_of_dict(continuing_dict)
	journey_id = current_path_details[0]
	been_set = current_path_details[1][0]
	current_path = current_path_details[1][1]
	current_route_id = current_path[-1]
	# termination condition
	if current_route_id == end_route_id:
		return [True, {journey_id: current_path_details}]
	else:
		# get the information about the next possible routes
		next_list = time_unit_connections_dict[current_route_id]
		# iterate over possible next routes
		for next_route_id in next_list:
			# make sure we haven't been on it before
			if next_route_id not in been_set:
				# add to the been set
				been_set.add(next_route_id)
				# create a new journey id
				journey_id = journey_id_list[-1] + 1
				journey_id_list.append(journey_id)
				# populate ending_dict
				new_path = list()
				for item in current_path:
					new_path.append(item)
				new_path.append(next_route_id)
				continuing_dict[journey_id] = [been_set, new_path]
	# return
	if not continuing_dict:
		new_path = list()
			for item in current_path:
				new_path.append(item)
			journey_path.append("There is no path from {} to {}".format(start_route_id, end_route_id))
			continuing_dict[journey_id] = [been_set, new_path]
			[True, continuing_dict]
	else:
		return [False, continuing_dict]



# def continue_journey(journey_id_list, journies_dict, been_list, end_route_id, time_unit_connections_dict):
# 	# sort journies so we know which is the shortest
# 	starting_dict = journies_dict
# 	# temp_dict that is the return object
# 	ending_dict = dict()
# 	# iterate over items in starting_dict
# 	for journey_id in starting_dict:
# 		# details
# 		path_details = starting_dict[journey_id]
# 		next_route_id = path_details[-1]
# 		# if the next_stop is our destination, then we have our route
# 		if next_route_id == end_route_id:
# 			ending_dict = dict()
# 			ending_dict[journey_id] = path_details
# 			return [True, ending_dict]
# 		# otherwise, we create the next set of possible paths
# 		else:
# 			# we get the information about the next possible routes
# 			next_list = time_unit_connections_dict[next_route_id]
# 			# iterate over possible next stops
# 			for next_route_id in next_list:
# 				if next_route_id not in been_list:
# 					# add to the been_list
# 					been_list.append(next_route_id)
# 					# create a new journey id
# 					journey_id = journey_id_list[-1] + 1
# 					journey_id_list.append(journey_id)
# 					# populate ending_dict
# 					new_details = copy.deepcopy(path_details)
# 					new_details.append(next_route_id)
# 					ending_dict[journey_id] = new_details
# 	# return
# 	if not ending_dict:
# 		return [True, {0: None}]
# 	else:
# 		return [False, ending_dict]



def find_shortest_path(start_route_id, end_route_id, time_unit_connections_dict):
	# data objects
	found_shortest_path = False
	journey_id_list = []
	journies_dict = dict()
	# start
	result = start_journey(start_route_id, end_route_id, time_unit_connections_dict, journey_id_list)
	journies_dict = result[1]
	found_shortest_path = result[0]
	# continue
	while found_shortest_path is False:
		result = continue_journey(journey_id_list, journies_dict, end_route_id, time_unit_connections_dict)
		found_shortest_path = result[0]
		journies_dict = result[1]
	# modify the return object
	journey_path = None
	for journey_id in journies_dict:
		journey_path = journies_dict[journey_id]
	# return
	return journey_path



def find_shortest_path_candidates_from_multiple_options(path_possibilities, time_unit_connections_dict):
	minimum_length = 10000000000000
	reduced_path_possibilities = list()
	for pp in path_possibilities:
		start_route_id = pp[0]
		end_route_id = pp[1]
		sp = find_shortest_path(start_route_id, end_route_id, time_unit_connections_dict)
		length = len(sp)
		if length < minimum_length:
			minimum_length = length
			reduced_path_possibilities = list()
			reduced_path_possibilities.append(sp)
		elif length == minimum_length:
			reduced_path_possibilities.append(sp)
		else:
			pass
	return reduced_path_possibilities