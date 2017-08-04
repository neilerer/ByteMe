# imports
import data_1_linked_list as d1
import data_2_possible_paths as d2
import pathfinder_1_possible_paths as p1



# source data
stop_dict = d1.linked_list_for_export()
possible_paths_dict = d2.possible_paths()


# reference data
all_stops_list = [stop for stop in stop_dict]
been_list = []
journey_id_list = []


def get_possible_paths(start, end, stop_dict, possible_paths_dict):
	path_possible_output = p1.path_possible(start, end, stop_dict, possible_paths_dict)
	# set_of_possible_paths
	return p1.possible_paths_for_pathfinder(path_possible_output)

# print(get_possible_paths(27, 72, stop_dict, possible_paths_dict))



def route_ok_start(route, set_of_possible_paths):
	for pair in set_of_possible_paths:
		for singleton in pair:
			if route == singleton:
				return True
	return False


def ok_routes_continue(current_route, route_tuple):
	try:
		current_index = route_tuple.index(current_route)
		next_route = route_tuple[current_index + 1]
		return [current_route, next_route]
	except:
		return [current_route]


def start_journey(start_stop_id, end_stop_id, stop_dict, been_list, journey_id_list, possible_path):
	if start_stop_id == end_stop_id:
		return [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "n/a")]]}]
	else:
		if possible_path[0]:
			set_of_possible_paths = possible_path[1]
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
				if next_stop_id not in been_list and route_ok_start(next_route, set_of_possible_paths):
					# record the journey_id
					journey_id_list.append(journey_id)
					# create the journey details
					temp_dict[journey_id] = [time_to_next_stop_id, [quadruple]]
					# increment the journey_id
					journey_id += 1
			return [False, temp_dict]
		else:
			return [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "not possible")]]}]

# possible_path = get_possible_paths(27, 72, stop_dict, possible_paths_dict)
# print(start_journey(27, 72, stop_dict, been_list, journey_id_list, possible_path))


