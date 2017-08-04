# imports
import copy
import data_1_linked_list as d1
import data_2_possible_paths as d2
import pathfinder_1_possible_paths as p1
import merge_sort



# source data
stop_dict = d1.linked_list_for_export()
possible_paths_dict = d2.possible_paths()

# reference data
all_stops_list = [stop for stop in stop_dict]



def get_possible_paths(start, end, stop_dict, possible_paths_dict):
	path_possible_output = p1.path_possible(start, end, stop_dict, possible_paths_dict)
	# set_of_possible_paths
	return p1.possible_paths_for_pathfinder(path_possible_output)

def accceptable_next_routes(set_of_possible_paths):
	next_route_dict = dict()
	for container in set_of_possible_paths:
		length = len(container)
		for i in range(0, length - 1, 1):
			if container[i] in next_route_dict:
				next_route_dict[container[i]].add(container[i + 1])
			else:
				next_route_dict[container[i]] = {container[i + 1]}
			next_route_dict[container[length - 1]] = container[length - 1]
	return next_route_dict

# print(get_possible_paths(27, 72, stop_dict, possible_paths_dict))



# def route_ok_start(route, set_of_possible_paths):
# 	for pair in set_of_possible_paths:
# 		for singleton in pair:
# 			if route == singleton:
# 				return True
# 	return False

def start_journey(start_stop_id, end_stop_id, stop_dict, been_list, journey_id_list, possible_path):
	if start_stop_id == end_stop_id:
		return [True, {1: [0.00, [(start_stop_id, "n/a", end_stop_id, "n/a")]]}]
	else:
		if possible_path[0]:
			set_of_possible_paths = possible_path[1]
			next_route_dict = accceptable_next_routes(set_of_possible_paths)
			# temp_dict
			temp_dict = dict()
			# instantiate journey_id
			try:
				journey_id = journey_id_list[-1] + 1
			except:
				journey_id = 0
			# record that we've been to this bus stop
			been_list.append(start_stop_id)
			# find the data we will use to start our journies
			list_of_next_quadruples = stop_dict[start_stop_id]
			# populate journies_dict
			for quadruple in list_of_next_quadruples:
				current_stop_id = quadruple[0]
				next_route = quadruple[1]
				next_stop_id = quadruple[2]
				time_to_next_stop_id = quadruple[3]
				# check if we've already been there
				if next_stop_id not in been_list and next_route in next_route_dict:
					# record the journey_id
					journey_id_list.append(journey_id)
					# create the journey details
					temp_dict[journey_id] = [time_to_next_stop_id, [quadruple]]
					# increment the journey_id
					journey_id += 1
			return [False, temp_dict]
		else:
			return [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "not possible")]]}]

# been_list = []
# journey_id_list = []
# journies_dict = dict()
# possible_path = get_possible_paths(27, 72, stop_dict, possible_paths_dict)
# journies_dict = start_journey(27, 72, stop_dict, been_list, journey_id_list, possible_path)[1]



def route_ok_continue(current_route, proposed_route, set_of_possible_paths):
	if current_route == proposed_route:
		return True
	else:
		for pair in set_of_possible_paths:
			if current_route in pair:
				cr_index = pair.index(current_route)
				if proposed_route == pair[cr_index + 1]:
					return True
		return False

def continue_journey(journey_id_list, journies_dict, been_list, end_stop_id, stop_dict, possible_path):
	# sort journies so we know which is the shortest
	starting_dict = merge_sort.merge_sort_journies_dict(journies_dict)
	# temp_dict that is the return object
	temp_dict = dict()
	# delete list
	delete_list = set()
	# iterate over items in starting_dict
	for jid in starting_dict:
		# details
		starting_details = starting_dict[jid]
		journey_time = starting_details[0]
		journey_details = starting_details[1]
		start_stop_id = journey_details[-1][0]
		current_route = journey_details[-1][1]
		next_stop_id = journey_details[-1][2]
		next_stop_journey_time = journey_details[-1][3]
		# skip if the next_stop has been visted before
		if next_stop_id in been_list:
			pass
		# if the next_stop is our destination, then we have our route
		elif next_stop_id == end_stop_id:
			temp_dict = dict()
			temp_dict[jid] = starting_details
			return [True, temp_dict]
		# otherwise, we create the next set of possible paths
		else:
			# we get the information about the next possible stop
			next_stop_details = stop_dict[next_stop_id]
			# iterate over possible next stops
			for next_stop_detail in next_stop_details:
				nsd_current_id = next_stop_detail[0]
				nsd_route = next_stop_detail[1]
				nsd_next_id = next_stop_detail[2]
				nsd_journey_time = next_stop_detail[3]
				# if the stop has not been visited
				set_of_possible_paths = possible_path[1]
				next_route_dict = accceptable_next_routes(set_of_possible_paths)
				if nsd_next_id not in been_list and (nsd_next_id != start_stop_id) and nsd_route in next_route_dict[current_route]: #and route_ok_continue(current_route, nsd_route, possible_path[1]):
					delete_list.add(jid) # we've extended this journey, so after temp_dict is full, delete this entry
					journey_id = journey_id_list[-1] + 1
					journey_id_list.append(journey_id)
					temp_details = copy.deepcopy(journey_details)
					temp_details.append(next_stop_detail)
					temp_dict[journey_id] = [journey_time + nsd_journey_time, temp_details]
				# if the stop has been visited, we don't modify the journey
				else:
					temp_dict[jid] = starting_details
	# delete journeys we don't need to explore
	delete_list = list(delete_list)
	for jid in delete_list:
		try:
			del temp_dict[jid]
		except:
			pass
	# return
	return [False, temp_dict]



def find_shortest_path(start_stop_id, end_stop_id, stop_dict, possible_paths_dict):
	shortest_path = None
	found_shortest_path = False
	this_been_list = []
	this_journey_id_list = []
	this_journies_dict = dict()
	possible_path = get_possible_paths(start_stop_id, end_stop_id, stop_dict, possible_paths_dict)
	# print(accceptable_next_routes(possible_path[1]))

	result = start_journey(start_stop_id, end_stop_id, stop_dict, this_been_list, this_journey_id_list, possible_path)
	this_journies_dict = result[1]

	while found_shortest_path is False:
		result = continue_journey(this_journey_id_list, this_journies_dict, this_been_list, end_stop_id, stop_dict, possible_path)
		found_shortest_path = result[0]
		this_journies_dict = result[1]

	return this_journies_dict


def find_shortest_path_review(all_stops_list):
	for stop in all_stops_list:
		for other_stop in all_stops_list:
			print(stop, other_stop)
			print(find_shortest_path(stop, other_stop, stop_dict, possible_paths_dict))
			print("")



# if __name__ == "__main__":
# 	find_shortest_path_review(all_stops_list)
	# print(all_stops_list)
	# print(possible_paths_dict)
	# for item in stop_dict:
	# 	print(item)
	# 	print(stop_dict[item])
	# print(find_shortest_path(20, 42, stop_dict, possible_paths_dict))