# imports
import os
import general
import merge_sort
import generate_routes

"""
This code determines the order of bus stops by using the conditional probability of who is a neighbour.
"""



def unique_stops(routes):
	"""
	Purpose
	- generate a list of unique stops for all the routes in a JPI file

	Input
	- output of generate_routes.routes(file_name)

	Output
	- a list of the unique stops for a given JPI
	-- each element is a string

	"""
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



def left_neighbour(stop_id, route):
	"""
	Purpose
	- determines who the left neighbour is of a stop_id in a given route

	Inputs
	- stop_id
	-- string value of a stop_id from a JPI file
	- route
	-- an array from the output of generate_routes.routes(file_name)

	Outputs
	- a string value of the left neighbour of the stop_id or None

	"""
	# see who the left neighbour is
	try:
		index = route.index(stop_id)
		# if the entry is at the far left, then it's the first entry; we pretend 'start' occurs to its left
		if index == 0:
			return 'start'
		# otherwise we return the value of the entry just next to the stop_id i.e. its left neighbour
		else:
			return route[index - 1]
	# if that can't happen, return None
	except:
		return None



def left_neighbours(stop_id, the_routes):
	"""
	Purpose
	- create an ordered dictionary of left neighbours of a stop_id in a JPI file

	Input
	- stop_id
	-- string value of a stop_id from a JPI file
	- the_routes
	-- output of generate_routes.routes(file_name)

	Output
	- a dictinoary
	- key:value : other_stop_id:probability of being left neighobur of stop_id

	"""
	# return object
	left_dict = {}
	# occurances
	occurances = 0
	# catalogue and tabulate the number of occurances of the left neighbour
	for route in the_routes:
		# determine the left neighbour
		neighbour = left_neighbour(stop_id, the_routes[route])
		# increment the tabulation of occurances
		occurances += 1
		# evalute if the neighbour is None; if not, add it to the appropriate dictionary entry
		if neighbour is not None:
			if neighbour in left_dict:
				left_dict[neighbour] += 1
			else:
				left_dict[neighbour] = 1
	# convert left_dict values to percentages of total appearances
	for neighbour in left_dict:
		left_dict[neighbour] = left_dict[neighbour] / occurances
	# sort the diciontary
	left_dict = merge_sort.merge_sort_dict_left_neighbours(left_dict)
	# return
	return left_dict



def left_neighbours_dict(the_routes, all_stops):
	"""
	Purpose
	- generate a dictionary with the output of left_neighbours(stop_id, the_routes) for each stop_id

	Input
	- the_routes
	-- output of generate_routes.routes(file_name)
	- all_stops
	-- a list of the unique stops for a given JPI

	Output
	- a dictionary with key:value stop_id:eft_neighbours(stop_id, the_routes) for each stop_id

	"""
	# return object
	neighbours_dict = {}
	# iterate over the unique stops
	for stop in all_stops:
		# add to the return object the ordered dictionary of left neighours, ordered by probability of being the left neighbour of the stop_id
		neighbours_dict[stop] = left_neighbours(stop, the_routes)
	# return
	return neighbours_dict



def find_right_neighbour(stop_id, neighbours_dict):
	"""
	Purpose
	- to identify the right neighbour of a stop_id

	Inputs
	- stop_id
	-- string value of a stop_id from a JPI file
	- neighbours_dict
	-- output of left_neighbours_dict(the_routes, all_stops)

	Output
	- the string value of the right neighbour of stop_id

	"""
	# initialise the return variable as Boolean
	start = False
	# this varible is a threshold: if a probability of being a left neighbour is below it, we drop that as a possible neighobur
	# 5% was chosen because the apparent "accidental" stops occurred well below 0.05% of the time, while all others had a minimum value of 10%
	start_value = 0.05
	# iterate over the output of left_neighbours_dict(the_routes, all_stops)
	for stop in neighbours_dict:
		# specify the dictionary to be used
		value_dict = neighbours_dict[stop]
		# get the highest probability neighbour
		temp = merge_sort.get_first_entry_of_dict(value_dict)
		# we find the highest probabilty left neighbour of each stop in neighbours dict
		# we will return the highest probability match of stop and stop_id
		# this means we've found the right neigbhour of stop_id
		if temp[0] == stop_id and temp[1] > start_value:
			start = stop
			start_value = temp[1]
	# return
	return start



def generate_bus_stops(neighbours_dict):
	# return object
	bus_stops = []
	# add the first stop
	first_stop = find_right_neighbour('start', neighbours_dict)
	# if the first stop is False, there are not stops
	if first_stop is False:
		return False
	else:
		bus_stops.append(first_stop)
	# iteratively find the rest
	keep_going = True
	while keep_going:
		# find the right neighobur
		neighbour = find_right_neighbour(bus_stops[-1], neighbours_dict)
		# check that the value is str i.e. there is a right neighbour
		if isinstance(neighbour, str):
			# add that stop to the list
			bus_stops.append(neighbour)
		else:
			# terminate the loop if no neighbour exists
			keep_going = False
	# return
	return bus_stops



if __name__ == "__main__":
	the_routes = generate_routes.routes("00010001.csv")
	all_stops = unique_stops(the_routes)
	my_dict = left_neighbours_dict(the_routes, all_stops)
	
	# for item in my_dict:
	# 	print(item)
	# 	print(my_dict[item])
	# 	print("")
	
	# print(find_right_neighbour("start", my_dict))
	# print(find_right_neighbour('226', my_dict))

	print(generate_bus_stops(my_dict))