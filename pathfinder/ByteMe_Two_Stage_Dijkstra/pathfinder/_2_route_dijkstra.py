# imports
import _0_data as data
import _1_route_mapping as rm
import time

def remove_first_entry_of_dict(d):
	# return d.pop(next(iter(d)))
	key = next(iter(d))
	value = d[key]
	d.pop(next(iter(d)))
	return [key, value]



def minimum_transfers(r_dict, weekday, time_unit, start_route, end_route):
	maximum_paths = 3
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
	start_route = '00670'
	end_route = '01451'

	start_time = time.time()
	print(start_route, end_route)
	end_time = time.time()
	route_set = minimum_transfers(r_dict, weekday, time_unit, start_route, end_route)
	for rs in route_set:
		print(rs)
	print("")
	print(end_time - start_time)


	# for start in r_dict[weekday][time_unit]:
	# 	for end in r_dict[weekday][time_unit]:
	# 		print(start, end)
	# 		route_set = minimum_transfers(r_dict, weekday, time_unit, start, end)
	# 		for rs in route_set:
	# 			print(rs)
	# 		print("")