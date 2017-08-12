# imports
import data
import merge_sort_paths
import _1_route_mapping as rm
import time



def get_other_direction(route):
	if route[4] == "1":
		return route[0:4]+"0"
	else:
		return route[0:4]+"1"



def minimum_transfers(r_dict, weekday, time_unit, start, end):
	visited = set()
	journey_id = -1
	path_dict = dict()
	candidate_paths = list()
	if start == end:
		return [start]
	for route in r_dict[weekday][time_unit][start]:
		journey_id += 1
		path_dict[journey_id] = [1, [start, route]]
	found = False
	while not found:
		# get current_details
		current_details = merge_sort_paths.remove_first_entry_of_dict(path_dict)[1]
		transfers = current_details[0]
		path = current_details[1]
		visited_route = path[-1]
		# check if we've completed the trip
		if visited_route == end:
			# for route in path:
			# 	reverse = get_other_direction(route)
			# 	if reverse not in path:
			# 		path.append(reverse)
			return path
		# mark that we've prior_stop as we'll now iterate over all its possible connections
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



if __name__ == "__main__":
	# data
	print("Loading model dict . . .")
	model_dict = data.get_model_data()
	print("Loaidng route dict . . .")
	r_dict = rm.routes_dict(model_dict)

	# test
	weekday = 0
	time_unit = 10
	maximum = 0
	for route in r_dict[weekday][time_unit]:
		for other_route in r_dict[weekday][time_unit]:
			start_time = time.time()
			minimum_transfers(r_dict, weekday, time_unit, route, other_route)
			end_time = time.time()
			result = end_time - start_time
			print("{} to {} took {}".format(route, other_route, result))
			print("")
			maximum = max(result, maximum)
	print("The maximum time to find a minimum transfer route was {}".format(maximum))