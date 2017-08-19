# imports
# import copy
import _0_0_data as data
import time


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
		# put the lowest time in first
		if d_1[key_1][0] < d_2[key_2][0]:
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

def merge_sort_journey_time(d_return):
	# d_return = copy.deepcopy(d_input)
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
		d_1 = merge_sort_journey_time(d_1)
		d_2 = merge_sort_journey_time(d_2)
		# sorting
		d_return = merge_on_journey_time(d_1, d_2)
	# return
	return d_return



def merge_on_journey_time_with_transfer_time(d_1, d_2, current_route):
	# create the return object 
	d_return = {}
	# get the latest stop until one dict is empty
	while len(d_1) > 0 and len(d_2) > 0:
		# create the traverse objects
		key_1, key_2 = next(iter(d_1)), next(iter(d_2))
		# first is not on the current route
		if d_1[key_1][1] != current_route and d_2[key_2][1] == current_route:
			if d_1[key_1][0] + 300 < d_2[key_2][0]:
				d_return[key_1] = d_1[key_1]
				del d_1[key_1]
			else:
				d_return[key_2] = d_2[key_2]
				del d_2[key_2]
		# second is not on the current route
		elif d_1[key_1][1] == current_route and d_2[key_2][1] != current_route:
			if d_1[key_1][0] < d_2[key_2][0] + 300:
				d_return[key_1] = d_1[key_1]
				del d_1[key_1]
			else:
				d_return[key_2] = d_2[key_2]
				del d_2[key_2]
		# both on current route or both not on current route
		else:
			if d_1[key_1][0] < d_2[key_2][0]:
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

def merge_sort_journey_time_with_transfer_time(d_return, current_route):
	# d_return = copy.deepcopy(d_input)
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
		d_1 = merge_sort_journey_time_with_transfer_time(d_1, current_route)
		d_2 = merge_sort_journey_time_with_transfer_time(d_2, current_route)
		# sorting
		d_return = merge_on_journey_time_with_transfer_time(d_1, d_2, current_route)
	# return
	return d_return



def dijkstra(stop_dict, weekday, time_unit, start_stop, end_stop):
	visited_stops = set()
	journey_id = -1
	path_dict = dict()
	# origin and destination are the same
	if start_stop == end_stop:
		return [0.00, {None:(None)}]
	# starting the path_dict
	for stop_tuple in stop_dict[weekday][time_unit][start_stop]:
		journey_id += 1
		# [time, route_list, route:(start, next, time, route)]
		path_dict[journey_id] = [stop_tuple[2], {stop_tuple[3]}, [stop_tuple]]
	# sort by journey time
	path_dict = merge_sort_journey_time(path_dict)
	visited_stops.add(start_stop)
	# begin the search
	found = False
	while not found:
		# current shortest data
		current_shortest = remove_first_entry_of_dict(path_dict)[1]
		current_shortest_time = current_shortest[0]
		current_details = current_shortest[2][-1]
		# details
		prior_stop = current_details[0]
		current_stop = current_details[1]
		time = current_details[2]
		current_route = current_details[3]
		# termination condition
		if current_stop == end_stop:
			return current_shortest
		elif current_stop is None:
			pass
		elif current_stop not in visited_stops:
			# mark that we've been here
			visited_stops.add(current_stop)
			# get all information from that stop
			for stop_tuple in stop_dict[weekday][time_unit][current_stop]:
				journey_id += 1
				# new route not visited_stops
				if stop_tuple[3] != current_route and stop_tuple[3] not in current_shortest[1]:
					# update the path
					new_path = current_shortest[2]
					new_path.append((stop_tuple[0], stop_tuple[1], stop_tuple[2] + 300, stop_tuple[3]))
					# update the routes we've been to
					new_route_set = current_shortest[1]
					new_route_set.add(stop_tuple[3])
					# update path_dict
					path_dict[journey_id] = [current_shortest_time + stop_tuple[2] + 300, new_route_set, new_path]
				# same route
				elif stop_tuple[3] == current_route:
					new_path = current_shortest[2]
					new_path.append(stop_tuple)
					path_dict[journey_id] = [current_shortest_time + stop_tuple[2], current_shortest[1], new_path]
				# we've already been on that route
				else:
					pass
		# sort by journey time
		path_dict = merge_sort_journey_time_with_transfer_time(path_dict, current_route)
		# print(path_dict)
		# print("")
		
		

if __name__ == "__main__":
	# data
	print("Loading stop_dict . . .")
	stop_dict = data.get_pickle_file("stop_dict.p")

	# inputs
	weekday = 0
	time_unit = 10
	start_stop = 400#3058
	end_stop = 4486#3057

	start_time = time.time()
	print(dijkstra(stop_dict, weekday, time_unit, start_stop, end_stop))
	print(time.time() - start_time)

