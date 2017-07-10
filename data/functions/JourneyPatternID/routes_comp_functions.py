# imports
import os


"""
This section produces a list of lists used to determine where the items of one array not present in another ought to go when placed into that other array
"""

"""
Returns an array that contains elements that are in secondary_array but not primary array
"""
def not_in_primary(primary_array, secondary_array):
	# not_in_array
	not_in_array = []
	# iterate over contenets of secondary_array
	for item in secondary_array:
		# check if item is in primary arrary
		if item not in primary_array:
			# append to not_in_array
			not_in_array.append(item)
	# return
	return not_in_array

"""
For an item in secondary array that is not in the primary array, determines the closest neighbour that is in primary array
"""
def closest_neighbour_in_primary(primary_array, secondary_array, value, side):
	# determine secondary_neighbours
	secondary_neighbours = list()
	if side == "left":
		# array of neighbours ordered from closest to furthest
		other_neighbours = secondary_array[0:secondary_array.index(value):1]
		other_neighbours.reverse()
	else:
		other_neighbours = secondary_array[secondary_array.index(value) + 1:]
	# find the closest side neighbour by working through secondary_arry
	neighbour_count = -1
	neighbour_found = False
	while neighbour_found is False:
		# increment the count
		neighbour_count += 1
		# iterate over other_neighbours
		try:
			neighbour_found = other_neighbours[neighbour_count] in primary_array
		# no neighour is in main_array
		except:
			return None
	# return
	return other_neighbours[neighbour_count]

"""
For given left and right neighbours, determines 
"""
# for a given element not in main, takes left and right closest neighbours to generate the range in main the value could fall within
def range_in_primary(primary_array, secondary_array, value):
	# left index
	try:
		left = closest_neighbour_in_primary(primary_array, secondary_array, value, "left")
		left_index = primary_array.index(left)
	except:
		# if left isn't in primary_array, set left_index to None
		left_index = None
	# right index
	try:
		right = closest_neighbour_in_primary(primary_array, secondary_array, value, "right")
		right_index = primary_array.index(right)
	except:
		# if right does not occur in primary index, we give the entire array from left_index onwards
		if isinstance(primary_array[left_index : : 1], int):
			return [primary_array[left_index : : 1]]
		return primary_array[left_index : : 1]
	# return
	if isinstance(primary_array[left_index : right_index + 1 : 1], int):
		return [value, left, right, [primary_array[left_index : right_index + 1 : 1]]]
	else:
		return [value, left, right, primary_array[left_index : right_index + 1 : 1]]

"""
Combines the functions in this section to create the details of the items not in primary_array, but in secondary_array
"""
def not_in_primary_details(primary_array, secondary_array):
	# objects
	not_in = not_in_primary(primary_array, secondary_array)
	stop_details_list = list()
	# 
	for stop in not_in:
		try:
			# data
			source = range_in_primary(primary_array, secondary_array, stop)
			left = source[1]
			right = source[2]
			primary_range = source[3]
			primary_range_length = len(primary_range)
			# details
			stop_details = [stop, left, right, primary_range, primary_range_length]
			stop_details_list.append(stop_details)
		except:
			pass
	# return [stop, left, right, primary_range, primary_range_length]
	return stop_details_list


"""
This section develops the functions that make a bus route
"""

# PAIRWISE CREATION OF A STOPID LIST
# determines if in a details list, there is a stop_detail with length 2
def primary_range_length_no_2(details):
	for stop_details in details:
		if stop_details[4] == 2:
			return False
	return True

# finds the minimum length of primary range in a detail list
def minimum_primary_range_length(details):
	minimum = details[0][4]
	for stop_details in details[1::1]:
		if stop_details[4] < minimum:
			minimum = stop_details[4]
	return minimum

# if the range in main is only two, this places the value from other into main between those values
def place_between(primary_array, left, right, value):
	left_array = primary_array[0 : primary_array.index(left) + 1 : 1]
	value_array = [value]
	right_array = primary_array[primary_array.index(right) : : 1]
	return left_array + value_array + right_array

def primary_range_length_2_action(primary_array, stop_details):
	# data
	stop = stop_details[0]
	left = stop_details[1]
	right = stop_details[2]
	primary_range = stop_details[3]
	primary_range_length = stop_details[4]		
	# actions
	if primary_range_length == 2:
		if left is None:
			# stop is know to be the first stop
			primary_array = [stop] + primary_array
		elif right is None:
			# stop is known to be beyond the last element of the main_array
			primary_array.append(stop)
		else:
			# stop is known to be between and contiguous with two elements in main_array
			primary_array = place_between(primary_array, left, right, stop)
	else:
		# could be in at least two places in main_array
		pass
	# return
	return primary_array

def pairwise_stop_id_list_length_2(primary_array, secondary_array):
	# create the list of details
	details = not_in_primary_details(primary_array, secondary_array)
	# termination condition
	termination_condition = primary_range_length_no_2(details)
	# continue until all stops whose exact location is immediately known
	while termination_condition is False:
		# iteration
		for stop_details in details:
			primary_array = primary_range_length_2_action(primary_array, stop_details)
		# create the list of details
		details = not_in_primary_details(primary_array, secondary_array)
		# termination condition
		try:
			termination_condition = primary_range_length_no_2(details)
		except:
			# this occurs when the details list is empty
			termination_condition = True
	# return
	return [primary_array, details]

def collect_primary_range_length_1_stop_ids(details):
	# create the lists
	left_list = []
	right_list = []
	# populate the lists
	for stop_details in details:
		# check if there is only one element in the range
		if stop_details[4] == 1:
			# check if it has no left neighbour i.e. should be the first on the list
			if stop_details[1] is None:
				left_list.append(stop_details[0])
			else:
				right_list.append(stop_details[0])
	# return
	return [left_list, right_list]


def stop_id_list_length_1_fix(primary_array, details):
	# data
	new_lists = collect_primary_range_length_1_stop_ids(details)
	left_list = new_lists[0]
	right_list = new_lists[1]
	# primary_array
	primary_array = left_list + primary_array + right_list
	# details
	new_details = []
	for stop_detail in details:
		if stop_detail[4] == 1:
			pass
		else:
			new_details.append(stop_detail)
	return [primary_array, new_details]


def remove_repeats_in_list(primary_array):
	new_array = []
	for item in primary_array:
		if item in new_array:
			pass
		else:
			new_array.append(item)
	return new_array


def route_for_jpi_on_weekday(weekday_dicts, weekday):
	# data
	data = weekday_dicts[weekday]
	key_list = [key for key in data]
	# preliminary matters
	primary_array = data[key_list[0]]
	secondary_array = data[key_list[1]]
	source = pairwise_stop_id_list_length_2(primary_array, secondary_array)
	final_array = source[0]
	details = source[1]
	# iterative calculation of route
	for key in key_list[2::1]:
		item = data[key]
		# length 2 issues
		source = pairwise_stop_id_list_length_2(final_array, item)
		final_array = source[0]
		# length 1 issues
		source = stop_id_list_length_1_fix(final_array, details)
		final_array = source[0]
	# get rid of repeats
	final_array = remove_repeats_in_list(final_array)
	# return
	return final_array