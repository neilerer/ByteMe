# imports
import _0_data as data
import _1_route_mapping as rm
import _2_route_dijkstra as rs
import time

# references
# stop_id : [(stop_id, next_stop_id, time, route), . . . ]



def remove_first_entry_of_dict(d):
	# return d.pop(next(iter(d)))
	key = next(iter(d))
	value = d[key]
	d.pop(next(iter(d)))
	return [key, value]

def merge_on_journey_time(d_1, d_2):
	# create the return object 
	d_return = {}
	# get the latest stop until one dict is empty
	while len(d_1) > 0 and len(d_2) > 0:
		# create the traverse objects
		key_1, key_2 = next(iter(d_1)), next(iter(d_2))
		# value of interest
		value_1, value_2 = d_1[key_1][0], d_2[key_2][0]
		# put the lowest time in first
		if value_1 < value_2:
			d_return[key_1] = d_1[key_1]
			del d_1[key_1]
		else:
			d_return[key_2] = d_2[key_2]
			del d_2[key_2]
	# add remaining elements
	while len(d_1) > 0:
		item = next(iter(d_1))
		d_return[item] = d_1[item]
		del d_1[item]
	while len(d_2) > 0:
		item = next(iter(d_2))
		d_return[item] = d_2[item]
		del d_2[item]
	# return
	return d_return

def merge_sort_on_journey_time(d_return):
	# objects
	d_1 = {}
	d_2 = {}
	length = len(d_return)
	middle = int(length / 2)

	# split the data into two parts
	if len(d_return) > 1:
		for i in range(0, middle, 1):
			next_item = next(iter(d_return))
			d_1[next_item] = d_return[next_item]
			del d_return[next_item]
		for i in range(middle, length, 1):
			next_item = next(iter(d_return))
			d_2[next_item] = d_return[next_item]
			del d_return[next_item]
		# recursion
		d_1 = merge_sort_on_journey_time(d_1)
		d_2 = merge_sort_on_journey_time(d_2)
		# sorting
		d_return = merge_on_journey_time(d_1, d_2)
	# return
	return d_return

def shortest_path(stop_dict, route_list, weekday, time_unit, start, end):
	# preliminary data
	visited_stop = set()
	journey_id = -1
	path_dict = dict()
	if start == end:
		return [start]
	# get the initial paths
	for stop_tuple in stop_dict[weekday][time_unit][start]:
		# only check those in the route tuple
		if stop_tuple[3] in route_list:
			# [journey time, list of routes been in, path]
			path_dict[journey_id] = [stop_tuple[2], [stop_tuple]]
	# sort path_dict by journey_time
	path_dict = merge_sort_on_journey_time(path_dict)
	# go until we find the shortest path
	while True:
		# get current_details
		try:
			current_details = remove_first_entry_of_dict(path_dict)[1]
		except:
			return None
		# termination condition
		# current_stop = current_details[1][-1][1]
		if current_details[1][-1][1] == end:
			return current_details
		# current_stop = current_details[1][-1][1]
		elif current_details[1][-1][1] is None:
			pass
		# current_stop = current_details[1][-1][1]
		elif current_details[1][-1][1] in visited_stop:
			pass
		# current_route = current_details[1][-1][3]
		elif current_details[1][-1][3] not in route_list:
			pass
		else:
			# current_stop = current_details[1][-1][1]
			for stop_tuple in stop_dict[weekday][time_unit][current_details[1][-1][1]]:
				# it must be on a designated route
				if stop_tuple[3] not in route_list:
					pass
				else:
					# increment journey_id
					journey_id += 1
					# update visited_stop with current_stop = current_details[1][-1][1]
					visited_stop.add(current_details[1][-1][1])
					# current_route = current_details[1][-1][3]
					if stop_tuple[3] == current_details[1][-1][3]:
						path_dict[journey_id] = [current_details[0] + stop_tuple[2], current_details[1] + [stop_tuple]]
					else:
						path_dict[journey_id] = [current_details[0] + stop_tuple[2] + 300, current_details[1] + [(stop_tuple[0], stop_tuple[1], stop_tuple[2] + 300, stop_tuple[3])]]
					# sort path_dict by journey_time
					path_dict = merge_sort_on_journey_time(path_dict)



def stop_routes(stop_quadruples_list):
	stop_routes_list = list()
	for quadruple in stop_quadruples_list:
		stop_routes_list.append(quadruple[3])
	return stop_routes_list

def get_possible_routes(stop_dict, r_dict, weekday, time_unit, start_stop, end_stop):
	# inputs
	possible_pairs = [(start, end) for start in stop_routes(stop_dict[weekday][time_unit][start_stop]) for end in stop_routes(stop_dict[weekday][time_unit][end_stop])]
	# generation
	possible_routes = list()
	for (start_route, end_route) in possible_pairs:
		possible_routes = possible_routes + rs.minimum_transfers(r_dict, weekday, time_unit, start_route, end_route)
	# sorting
	possible_routes.sort(key=len)
	return possible_routes



def the_shortest_path(stop_dict, r_dict, weekday, time_unit, start, end):
	possible_routes = get_possible_routes(stop_dict, r_dict, weekday, time_unit, start, end)
	shortest_path_dict = dict()
	for route_list in possible_routes:
		sp = shortest_path(stop_dict, route_list, weekday, time_unit, start, end)
		if sp is None:
			pass
		else:
			shortest_path_dict[tuple(route_list)] = sp
	# sort shorest_path_dict by journey_time
	shortest_path_dict = merge_sort_on_journey_time(shortest_path_dict)
	# because our front end will only manage one route suggestion
	sp = remove_first_entry_of_dict(shortest_path_dict)
	routes_used = list()
	for quadruple in sp[1][1]:
		if quadruple[3] not in routes_used:
			routes_used.append(quadruple[3])
	return [routes_used, sp[1]]



if __name__ == "__main__":
	# data
	print("Loading stop_dict . . .")
	stop_dict = data.get_pickle_file("stop_dict.p")
	print("Loading route_dict . . .")
	r_dict = rm.routes_dict(stop_dict)

	# inputs
	weekday = 0
	time_unit = 10
	start = 400
	end = 807

	start_time = time.time()
	sp = the_shortest_path(stop_dict, r_dict, weekday, time_unit, start, end)
	end_time = time.time() - start_time

	print("")
	print("Routes used")
	print(sp[0])
	print("")
	print("Journey Time")
	print(sp[1][0])
	print("")
	print("The Shortest Path")
	for quadruple in sp[1][1]:
		print(str(quadruple))
	print("")