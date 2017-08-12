# imports
import data
import dijkstra_merge_sort
import time



def weekday_list():
	model_dict = data.get_model_data()
	wd_list = list()
	for weekday in model_dict:
		wd_list.append(weekday)
	return wd_list

def time_unit_list(wd_list):
	model_dict = data.get_model_data()
	tu_list = set()
	for weekday in wd_list:
		for time_unit in model_dict[weekday]:
			tu_list.add(time_unit)
	return list(tu_list)

def stop_id_dict():
	model_dict = data.get_model_data()
	stop_id_dict = dict()
	for weekday in model_dict:
		stop_id_dict[weekday] = dict()
		for time_unit in model_dict[weekday]:
			stop_id_dict[weekday][time_unit] = list()
			for stop_id in model_dict[weekday][time_unit]:
				stop_id_dict[weekday][time_unit].append(stop_id)
	return stop_id_dict



def stop_routes(stop_quadruples_list):
	stop_routes_list = list()
	for quadruple in stop_quadruples_list:
		stop_routes_list.append(quadruple[3])
	return stop_routes_list

def shortest_path(weekday, time_unit, start, end, model_dict):
	starting_quadruples = model_dict[weekday][time_unit][start]
	end_routes_list = stop_routes(starting_quadruples)
	visited = set()
	journey_id = -1
	path_dict = dict()
	for quadruple in model_dict[weekday][time_unit][start]:
		journey_id += 1
		path_dict[journey_id] = [0, 0.00, [quadruple]]
	found = False
	while not found:
		# path_dict
		path_dict = dijkstra_merge_sort.merge_sort(path_dict, end_routes_list)
		# get current shortet journey
		current_journey_details = dijkstra_merge_sort.remove_first_entry_of_dict(path_dict)[1]
		transfers = current_journey_details[0]
		total_time = current_journey_details[1]
		quadruple_list = current_journey_details[2]
		# current_stop_details
		current_stop_details = quadruple_list[-1]
		prior_stop = current_stop_details[0]
		current_stop = current_stop_details[1]
		prior_to_next_stop_time = current_stop_details[2]
		current_route = current_stop_details[3]
		# check if we've completed the trip
		if end == current_stop:
			found = True
			return current_journey_details	
		# mark that we've prior_stop as we'll now iterate over all its possible connections
		visited.add(prior_stop)
		# iterate over all possible connections of the prior_stop
		for quadruple in model_dict[weekday][time_unit][current_stop]:
			# unpack
			further_stop = quadruple[1]
			further_journey_time = quadruple[2]
			further_route = quadruple[3]
			# determine what to do
			if further_stop in visited or further_stop is None or (current_route in end_routes_list and further_route not in end_routes_list):
				pass
			else:
				journey_id += 1
				if current_route != further_route:
					path_dict[journey_id] = [transfers + 1, total_time + further_journey_time + 300, quadruple_list + [(current_stop, further_stop, further_journey_time + 300, further_route)]]
				else:
					path_dict[journey_id] = [transfers, total_time + further_journey_time, quadruple_list + [(current_stop, further_stop, further_journey_time, further_route)]]


if __name__ == "__main__":
	# data
	print("Loading the model data . . .")
	model_dict = data.get_model_data()
	print("Loading the weekday list")
	wd_list = weekday_list()
	print("Loading the time_unit list")
	tu_list = time_unit_list(wd_list)
	print("Loading the stop id dict")
	si_dict = stop_id_dict()
	print("")

	# test 1
	weekday = 0
	time_unit = 10
	start = 768
	end = 772
	time_start = time.time()
	sp = shortest_path(weekday, time_unit, start, end, model_dict)
	run_time = time.time() - time_start
	print("{} to {} took {}".format(start, end, run_time))
	print(sp)
	print("")

	# test 2
	weekday = 0
	time_unit = 10
	start = 768
	end = 400
	time_start = time.time()
	sp = shortest_path(weekday, time_unit, start, end, model_dict)
	run_time = time.time() - time_start
	print("{} to {} took {}".format(start, end, run_time))
	print(sp)
	print("")







# def update_from_path_dict_entry(journey_id, path_dict, stop_set, route_dict):
# 	# data
# 	data = path_dict[journey_id]
# 	transfers = data[0]
# 	time = data[1]
# 	quadruple = data[2][-1]
# 	current_stop = quadruple[0]
# 	next_stop = quadruple[1]
# 	time = quadruple[2]
# 	route = quadruple[3]
# 	# stop_set
# 	stop_set.add(current_stop)
# 	# route_dict
# 	if journey_id in route_dict:
# 		if route in route_dict[journey_id]:
# 			route_dict[journey_id].append(route)
# 		else:
# 			route_dict[journey_id] = [route]
# 	else:
# 		route_dict[journey_id] = [route]





# def shortest_path(weekday, time_unit, start, end, model_dict, end_routes_list, journey_id_list, journey_id, stop_set, route_dict, path_dict):
# 	# get the current shortest path
# 	dijkstra_merge_sort.merge_sort(path_dict)
# 	current_shortest_path = dijkstra_merge_sort.remove_first_entry_of_dict(path_dict)[1]
# 	# data
# 	transfers = current_shortest_path[0]
# 	time = current_shortest_path[1]
# 	quadruple_list = current_shortest_path[2]
# 	current_quadruple = quadruple_list[-1]
# 	current_stop = current_quadruple[0]
# 	next_stop = current_quadruple[1]
# 	journey_time = current_quadruple[2]
# 	current_route = current_quadruple[3]
# 	old_route_dict_entry = route_dict[journey_id]
# 	# update stop_set
# 	stop_set.add(next_stop)
# 	# iterate over next_stop values
# 	for quadruple in model_dict[weekday][time_unit][next_stop]:
# 		# unpack
# 		starting_stop = quadruple[0]
# 		further_stop = quadruple[1]
# 		further_time = quadruple[2]
# 		further_route = quadruple[3]
# 		# exit conditions
# 		if (further_stop is None or starting_stop is None) or (further_stop in stop_set) or (further_route in route_dict[journey_id] and further_route != current_route):
# 			continue
# 		elif starting_stop == end:
# 			return [True, current_shortest_path]
# 		else:
# 			# journey_id
# 			journey_id = journey_id_list[-1] + 1
# 			journey_id_list.append(journey_id)
# 			# path_dict
# 			time_fudge = 300 # CD to supply input tables
# 			if current_route != further_route:
# 				new_quadruple = quadruple_list + [(starting_stop, further_stop, further_time + time_fudge, further_route)]
# 				path_dict[journey_id] = [transfers + 1, time + further_time + time_fudge, new_quadruple]
# 			else:
# 				new_quadruple = quadruple_list + [(starting_stop, further_stop, further_time, further_route)]
# 				path_dict[journey_id] = [transfers, time + further_time, new_quadruple]
# 			# route_dict
# 			if journey_id in route_dict:
# 				route_dict[journey_id] += [further_route]
# 			else:
# 				route_dict[journey_id] = old_route_dict_entry + [further_route]
# 	# return
# 	return [False, path_dict]



# def dijkstra(weekday, time_unit, start, end, model_dict):
# 	# quick check
# 	if start == end:
# 		return [True, [0, 0.00, "n/a"]]
# 	# data
# 	end_routes_list = stop_routes(stop_quadruples(weekday, time_unit, end, model_dict))
# 	journey_id_list = [-1]
# 	journey_id = journey_id_list[-1]
# 	stop_set = set()
# 	route_dict = dict()
# 	# path_dict
# 	path_dict = dict()
# 	for quadruple in model_dict[weekday][time_unit][start]:
# 		journey_id += 1
# 		journey_id_list.append(journey_id)
# 		transfers = 0
# 		time = quadruple[2]
# 		path_dict[journey_id] = [transfers, time, [quadruple]]
# 		update_from_path_dict_entry(journey_id, path_dict, stop_set, route_dict)
# 	# shortest path
# 	found = False
# 	while found == False:
# 		result = shortest_path(weekday, time_unit, start, end, model_dict, end_routes_list, journey_id_list, journey_id, stop_set, route_dict, path_dict)
# 		found = result[0]
# 		path_dict = result[1]
# 		print(path_dict)
# 	# return
# 	return path_dict