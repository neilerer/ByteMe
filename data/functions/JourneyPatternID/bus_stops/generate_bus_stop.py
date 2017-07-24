# imports
import os
import general
import merge_sort
import generate_routes


# uniqute values of StopID
def unique_stops(routes):
	# list of stops
	stops = []
	# iterate over the lists
	for stop_list in routes:
		# iterate over the elements in the list
		for stop in routes[stop_list]:
			# check for inclusion
			if stop not in stops:
				# add if not already there
				stops.append(stop)
	# return stops
	return stops



# of the times it occurs, how often is it first
def pct_first(stop_id, routes, position):
	"""
	Purpose
	- to determine the weighted occurances of a stop_id on a jpi for a given weekday
	Inputs
	- stop_id
	- specific_weekday_routes
	-- output of routes_weekday_list()
	- position
	-- position we care about
	Outputs
	- a floating number greater than or equal to 0
	"""
	# count the number of times the stop_id occurs
	occurances = 0
	# count the number of times the stop_id occurs in position
	pos = 0
	# iterate over the routes
	for route in routes:
		try:
			# find the index; stop_id will occur only once in each route
			index = routes[route].index(stop_id)
			# increment occurances
			occurances += 1
			# if its in the position
			if index == position:
				# increment pos
				pos += 1
		except:
			# if stop_id isn't in the route
			pass
	try:
		# return the weighted occurances of stop_id
		# if it occurs only once and in the position, don't count it
		if pos == 1 and occurances == 1:
			return 0
		else:
			return (pos / occurances) * pos
	except:
		# return zero if stop_id never occurred
		return 0


the_routes = generate_routes.routes("00010001.csv")
all_stops = unique_stops(the_routes)

# for item in the_routes:
# 	print(the_routes[item])
# print("")
for stop in all_stops:
	print("{}: {}".format(stop, pct_first(stop, the_routes, 0)))


def who_is_first(all_stops, routes, position):
	# dictionary that will hold each stop and it's rank of occuring first as value
	stop_dict = {stop:False for stop in all_stops}
	# iterate over each unique stop
	for stop in all_stops:
		# use pct_first to add the value
		stop_dict[stop] = pct_first(stop, routes, position)
	# sort the dictionary by order of most often first to least often first
	stop_dict = merge_sort.merge_sort_dict_who_is_first(stop_dict)
	# return the dictionary
	return stop_dict


# print(who_is_first(all_stops, the_routes, 0))


def remove_element_from_list(element, array):
	indices = []
	index = 0
	for item in array:
		if item == element:
			indices.append(index)
		index += 1
	indices.reverse()
	for i in indices:
		array.pop(i)
	return array


def bus_stops(all_stops, routes):
	# termination condition
	termination_length = len(all_stops)
	# return object
	bus_stop_list = []
	# count
	count = 0
	# loop until termination condition is achieved
	# while len(bus_stop_list) < termination_length:
	while count < termination_length:
		# make the sorted dictionary of stops
		stop_dict = who_is_first(all_stops, routes, 0)
		# obtain a stop candidate
		stop = merge_sort.remove_first_entry_of_dict(stop_dict)[0]
		# termination condition
		in_list = (stop in bus_stop_list)
		# loop until termination is achieved
		while in_list:
			# obtain a stop candidate
			stop = merge_sort.remove_first_entry_of_dict(stop_dict)[0]
			# check termination condition
			in_list = (stop in bus_stop_list)
		# append the successful stop
		bus_stop_list.append(stop)
		# remove stop from unique_stops (we will no longer consider it)
		all_stops.pop(all_stops.index(stop))
		# remove stop from weekday_routes (we will no longer consdier it)
		for item in routes:
			routes[item] = remove_element_from_list(stop, routes[item])
		# increment the count
		count += 1
	# return
	return bus_stop_list

print(bus_stops(all_stops, the_routes))