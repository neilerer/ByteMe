# imports
# imports
import data
import dijkstra_merge_sort
import _1_route_mapping as rm
import _2_route_planning as rp
import time
from operator import itemgetter



def stop_routes(stop_quadruples_list):
	stop_routes_list = list()
	for quadruple in stop_quadruples_list:
		stop_routes_list.append(quadruple[3])
	return stop_routes_list

def get_possible_routes(model_dict, r_dict, weekday, time_unit, start_stop, end_stop):
	# data
	start_routes = stop_routes(model_dict[weekday][time_unit][start_stop])
	end_routes = stop_routes(model_dict[weekday][time_unit][end_stop])
	# inputs
	possible_pairs = [(start, end) for start in start_routes for end in end_routes]
	# generation
	possible_routes = [rp.minimum_transfers(r_dict, weekday, time_unit, start_route, end_route) for (start_route, end_route) in possible_pairs]
	# sorting
	possible_routes.sort(key=len)
	return possible_routes


def get_route_data(route_list, json_data, weekday, time_unit):
	data_dict = dict()
	for route in route_list:
		data_dict[route] = list()
	for route in route_list:
		for jpi in json_data:
			if jpi[0:5] == route:
				for key in json_data[jpi]:
					key_list = key.strip().split("-")
					position = int(key_list[0])
					stop = int(key_list[1])
					wd = int(key_list[2])
					tu = int(key_list[3])
					ctt = float(json_data[jpi][key])
					key_list.append(ctt)
					# 
					if wd == weekday and tu == time_unit:
						data_dict[jpi[0:5]].append((position, stop, ctt))
	for route in data_dict:
		data_dict[route].sort(key=itemgetter(0))
	# return
	return data_dict



def shortest_path(model_dict, route_list, weekday, time_unit, start, end):
	starting_quadruples = model_dict[weekday][time_unit][start]
	visited = {start}
	journey_id = -1
	path_dict = dict()
	for quadruple in model_dict[weekday][time_unit][start]:
		if quadruple[3] in route_list:
			journey_id += 1
			path_dict[journey_id] = [0, 0.00, [quadruple]]
		else:
			pass
	found = False
	while not found:
		path_dict = dijkstra_merge_sort.merge_sort(path_dict)
		print(len(path_dict))
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
		visited.add(current_stop)
		# iterate over all possible connections of the prior_stop
		for quadruple in model_dict[weekday][time_unit][current_stop]:
			# unpack
			further_stop = quadruple[1]
			further_journey_time = quadruple[2]
			further_route = quadruple[3]
			if further_route in route_list and further_stop is not None and further_stop not in visited:
				journey_id += 1
				if current_route != further_route:
					path_dict[journey_id] = [transfers + 1, total_time + further_journey_time + 300, quadruple_list + [(current_stop, further_stop, further_journey_time + 300, further_route)]]
				else:
					path_dict[journey_id] = [transfers, total_time + further_journey_time, quadruple_list + [(current_stop, further_stop, further_journey_time, further_route)]]



if __name__ == "__main__":
	# data
	print("Loading model dict . . .")
	model_dict = data.get_model_data()
	print("Loading route dict . . .")
	r_dict = rm.routes_dict(model_dict)
	print("Loading JSON data . . .")
	json_data = data.get_actual_model_data()

	weekday = 0
	time_unit = 10
	start = 772
	end = 400
	r_dict = get_possible_routes(model_dict, r_dict, weekday, time_unit, start, end)

	print(r_dict)
	route_list = r_dict[-1]
	print(route_list)
	grb = get_route_data(route_list, json_data, weekday, time_unit)
	
	if len(route_list) == 1:
		print("just one; link up via stops")
	else:
		for i in range(1, len(route_list), 1):
			first_route = route_list[i - 1]
			second_route = route_list[i]
			for f_tuple in grb[first_route]:
				for s_tuple in grb[second_route]:
					f_stop = f_tuple[1]
					s_stop = s_tuple[1]
					if f_stop == s_stop:
						print(first_route, f_tuple, second_route, s_tuple)
