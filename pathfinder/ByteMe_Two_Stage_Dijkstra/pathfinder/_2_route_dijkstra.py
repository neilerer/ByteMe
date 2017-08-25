# imports
import _0_data as data
import _1_route_mapping as rm
import time



def remove_first_entry_of_dict(d):
	key = next(iter(d))
	value = d[key]
	d.pop(next(iter(d)))
	return [key, value]



def is_subset_for_two_lists(l_1, l_2):
	if len(l_2) < len(l_1):
		return False
	else:
		for i in range(0, len(l_1), 1):
			if l_1[i] != l_2[i]:
				return False
	return True

def is_subset_for_multiple_lists(l_1, list_of_lists):
	for other_lists in list_of_lists:
		if is_subset_for_two_lists(l_1, other_lists):
			return True
	return False



def minimum_transfers(r_dict, weekday, time_unit, start_route, end_route):
	"""
	This function is is an implementation of Dijkstra's Algorithm
	Routes are nodes
	Edges connect routes that intersect and have weight 1, representing a transfer from one route to another
	"""
	maximum_paths = 1000
	possible_paths = list()
	visited = set()
	journey_id = -1
	path_dict = dict()
	candidate_paths = list()
	# check the simple case
	if start_route == end_route:
		possible_paths.append([start_route])
	# explore more complex possible paths
	for route in r_dict[weekday][time_unit][start_route]:
		journey_id += 1
		path_dict[journey_id] = [1, [start_route, route]]
	# mark that we've been on the start_route already
	visited.add(start_route)
	# develop non-trivial paths
	while not not path_dict and len(possible_paths) <= maximum_paths:
		# get current_details
		current_details = remove_first_entry_of_dict(path_dict)[1]
		transfers = current_details[0]
		path = current_details[1]
		visited_route = path[-1]
		# check if we've completed the trip
		if visited_route == end_route:
			possible_paths.append(path)
		else:
			# make sure this path has not already been explored
			if is_subset_for_multiple_lists(path, possible_paths):
				pass
			else:
				# mark that we've been to visted_route as we'll now iterate over all its possible connections
				visited.add(visited_route)
				# iterate over all possible connections of the prior_stop
				for route in r_dict[weekday][time_unit][visited_route]:
					if route in visited:
						pass
					else:
						journey_id += 1
						new_path = path + [route]
						new_transfers = transfers + 1
						path_dict[journey_id] = [new_transfers, new_path]
	return possible_paths



if __name__ == "__main__":
	stop_dict = data.get_pickle_file("stop_dict.p")
	r_dict = rm.routes_dict(stop_dict)

	# inputs
	weekday = 0
	time_unit = 10
	start_route = '00081' #'00590'
	end_route = '00130' #'00040'

	start_time = time.time()
	print(start_route, end_route)
	end_time = time.time()
	route_set = minimum_transfers(r_dict, weekday, time_unit, start_route, end_route)
	for rs in route_set:
		print(rs)
	print("")
	print(end_time - start_time)


