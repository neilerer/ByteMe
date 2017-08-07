# imports
import data_1_linked_list as d1
import data_2_possible_paths as d2
import pathfinder_1_possible_paths as p1



# source data
stop_dict = d1.linked_list_for_export()
possible_paths_dict = d2.possible_paths()



def accceptable_next_routes(list_of_possible_paths):
	next_route_dict = dict()
	for container in list_of_possible_paths:
		length = len(container)
		for i in range(0, length - 1, 1):
			if container[i] in next_route_dict:
				next_route_dict[container[i]].add(container[i + 1])
			else:
				next_route_dict[container[i]] = {container[i + 1]}
			next_route_dict[container[length - 1]] = container[length - 1]
	return next_route_dict

def get_possible_paths(start, end, stop_dict, possible_paths_dict):
	path_possible_output = p1.path_possible(start, end, stop_dict, possible_paths_dict)
	possible_paths_container = p1.possible_paths_for_pathfinder(path_possible_output)
	boolean = possible_paths_container[0]
	list_of_possible_paths = possible_paths_container[1]
	if boolean:
		return [True, accceptable_next_routes(list_of_possible_paths)]
	else:
		return [False, None]


# print(get_possible_paths(20, 72, stop_dict, possible_paths_dict))

# def accceptable_next_routes(list_of_possible_paths):
# 	next_route_dict = dict()
# 	for container in list_of_possible_paths:
# 		length = len(container)
# 		for i in range(0, length - 1, 1):
# 			if container[i] in next_route_dict:
# 				next_route_dict[container[i]].add(container[i + 1])
# 			else:
# 				next_route_dict[container[i]] = {container[i + 1]}
# 			next_route_dict[container[length - 1]] = container[length - 1]
# 	return next_route_dict
# list_of_possible_paths = get_possible_paths(20, 72, stop_dict, possible_paths_dict)[1]
# print(accceptable_next_routes(list_of_possible_paths))



def start_journey(start_stop_id, end_stop_id, stop_dict, been_list, journey_id_list, get_possible_paths_output):
	if start_stop_id == end_stop_id:
		return [True, {1: [0.00, [(start_stop_id, "n/a", end_stop_id, "n/a")]]}]
	else:
		possible = get_possible_paths_output[0]
		next_route_dict = get_possible_paths_output[1]
		if possible:
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
				if (next_stop_id not in been_list) and (next_route in next_route_dict):
					# record the journey_id
					journey_id_list.append(journey_id)
					# create the journey details
					temp_dict[journey_id] = [time_to_next_stop_id, [quadruple]]
					# increment the journey_id
					journey_id += 1
			return [False, temp_dict]
		else:
			return [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "not possible")]]}]