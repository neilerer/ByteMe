# imports
import data_1_linked_list as d1
import data_2_possible_paths as d2



# source data
stop_dict = d1.linked_list_for_export()
possible_paths_dict = d2.possible_paths()

# reference data
all_stops_list = [stop for stop in stop_dict]



def get_stop_routes(stop, stop_dict):
	source = stop_dict[stop]
	routes = []
	for quadruple in source:
		routes.append(quadruple[1])
	return routes

# print(get_stop_routes(72, stop_dict))



def path_possible(start, end, stop_dict, possible_paths_dict):
	start_routes = get_stop_routes(start, stop_dict)
	end_routes = get_stop_routes(end, stop_dict)
	possible_paths_list = []
	possible = False
	for s in start_routes:
		for e in end_routes:
			key = str(s) + "_" + str(e)
			if key in possible_paths_dict:
				possible = True
				pp = possible_paths_dict[key]
				possible_paths_list.append(pp)
	# path_possible_output
	return [possible, possible_paths_list]

# for stop in all_stops_list:
# 	for other_stop in all_stops_list:
# 		print(path_possible(stop, other_stop, stop_dict, possible_paths_dict))

def minimum_tuples_in_list(list_of_tuples):
	minimum = len(list_of_tuples[0])
	for t in list_of_tuples[0::1]:
		if len(t) < minimum:
			minimum = len(t)
	tuple_list = [t for t in list_of_tuples if len(t) == minimum]
	return tuple_list

def possible_paths_for_pathfinder(path_possible_output):
	boolean = path_possible_output[0]
	list_of_tuples = path_possible_output[1]
	if boolean:
		return [True, minimum_tuples_in_list(list_of_tuples)]
	else:
		return [False, []]

# a_possible_path = path_possible(27, 72, stop_dict, possible_paths_dict)
# print(possible_paths_for_pathfinder(a_possible_path))



if __name__ == "__main__":
	for stop in all_stops_list:
		for other_stop in all_stops_list:
			a_possible_path = path_possible(stop, other_stop, stop_dict, possible_paths_dict)
			a_set_of_possible_paths = possible_paths_for_pathfinder(a_possible_path)
			if a_set_of_possible_paths[0]:
				for pp in a_set_of_possible_paths[1]:
					print("{} to {} via {}".format(stop, other_stop, pp))
			else:
				print("{} to {} cannot happen".format(stop, other_stop))