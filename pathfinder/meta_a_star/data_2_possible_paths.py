# imports
import datetime
import pickle
import time
import copy
import data_1_linked_list as d1



def get_stop_linked_list():
	return d1.linked_list_for_export()



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

def route_connections_review(rc_dict):
	for route in rc_dict:
		print(route)
		print(rc_dict[route])
		print("")



def start_journey(start_route, end_route, rc_dict, been_list, journey_id_list):
	if start_route == end_route:
		return [True, {0: [start_route]}]
	# temp_dict
	temp_dict = dict()
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
		journey_id = 0
	# record that we've been to this bus stop
	been_list.append(start_route)
	# find the data we will use to start our journies
	list_of_next_routes = rc_dict[start_route]
	# populate routes_dict
	for route in list_of_next_routes:
		# check if we've already been there
		if route not in been_list:
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			temp_dict[journey_id] = [start_route, route]
			# increment the journey_id
			journey_id += 1
	return [False, temp_dict]

def continue_journey(journey_id_list, routes_dict, been_list, end_route_id, rc_dict):
	# sort journies so we know which is the shortest
	starting_dict = routes_dict
	# temp_dict that is the return object
	temp_dict = dict()
	# delete list
	delete_list = set()
	# iterate over items in starting_dict
	for jid in starting_dict:
		# details
		route_details = starting_dict[jid]
		next_route = route_details[-1]
		# skip if the next_stop has been visted before
		if next_route in been_list:
			pass
		# if the next_stop is our destination, then we have our route
		elif next_route == end_route_id:
			temp_dict = dict()
			temp_dict[jid] = route_details
			return [True, temp_dict]
		# otherwise, we create the next set of possible paths
		else:
			# we get the information about the next possible stop
			next_list = rc_dict[next_route]
			# iterate over possible next stops
			for next_route in next_list:
				# if the stop has not been visited
				if next_route not in been_list:
					delete_list.add(jid) # we've extended this journey, so after temp_dict is full, delete this entry
					journey_id = journey_id_list[-1] + 1
					journey_id_list.append(journey_id)
					temp_details = copy.deepcopy(route_details)
					temp_details.append(next_route)
					temp_dict[journey_id] = temp_details
				# if the stop has been visited, we don't modify the journey
				else:
					temp_dict[jid] = route_details
	# delete journeys we don't need to explore
	delete_list = list(delete_list)
	for jid in delete_list:
		try:
			del temp_dict[jid]
		except:
			pass
	# return
	return [False, temp_dict]

def find_shortest_path(start_route, end_route, rc_dict):
	this_shortest_path = None
	this_found_shortest_path = False
	this_been_list = []
	this_journey_id_list = []
	this_journies_dict = dict()

	result = start_journey(start_route, end_route, rc_dict, this_been_list, this_journey_id_list)
	this_journies_dict = result[1]
	this_found_shortest_path = result[0]


	while this_found_shortest_path is False:
		result = continue_journey(this_journey_id_list, this_journies_dict, this_been_list, end_route, rc_dict)
		this_found_shortest_path = result[0]
		this_journies_dict = result[1]

	this_shortest_path = this_journies_dict

	return this_shortest_path



def possible_paths():
	stop_linked_list = get_stop_linked_list()
	route_connections_dict = route_connections(stop_linked_list)
	been_list = list()
	journey_id_list = list()
	range_list = []

	pp_dict = dict()
	for start in route_connections_dict:
		for end in route_connections_dict:
			key = str(start) + "_" + str(end)
			sp = find_shortest_path(start, end, route_connections_dict)
			value = None
			for item in sp:
				value = sp[item]
			pp_dict[key] = tuple(value)
	return pp_dict

my_item = possible_paths()
for item in my_item:
	print(item)
	print(my_item[item])
	print("")

# if __name__ == "__main__":
# 	stop_linked_list = get_stop_linked_list()
# 	route_connections_dict = route_connections(stop_linked_list)
# 	print(route_connections_dict)

# 	been_list = list()
# 	journey_id_list = list()
# 	range_list = []
# 	first_range = range(-3, 0, 1)
# 	for i in first_range:
# 		range_list.append(i)
# 	second_range = range(1, 4, 1)
# 	for i in second_range:
# 		range_list.append(i)
# 	for f in range_list:
# 		for s in range_list:
# 			print(find_shortest_path(f, s, route_connections_dict))