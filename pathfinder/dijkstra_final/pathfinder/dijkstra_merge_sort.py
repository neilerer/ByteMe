# {0: [0, 61.83473320363646, [(768, 769, 61.83473320363646, '01451')]], 1: [0, 64.07522916619928, [(768, 2085, 64.07522916619928, '00471')]], 2: [0, 72.37828945081264, [(768, 769, 72.37828945081264, '046A1')]], 3: [0, 78.25674273527522, [(768, 769, 78.25674273527522, '039A0')]], 4: [0, 134.34609119887364, [(768, 772, 134.34609119887364, '084X1')]]}


# imports
import copy


"""
GET AND REMOVE FIRST ITEMS FROM A DICTIONARY
"""
def remove_first_entry_of_dict(d):
	# return d.pop(next(iter(d)))
	key = next(iter(d))
	value = d[key]
	d.pop(next(iter(d)))
	return [key, value]
#
def get_first_entry_of_dict(d):
	key = next(iter(d))
	value = d[key]
	return [key, value]



def merge_on_time(d_1, d_2):
	"""
	This functions merges two dictionaries (each of which are assumed to be sorted as desired)
	"""
	# create the return object 
	d_return = {}
	# get the latest stop until one dict is empty
	while len(d_1) > 0 and len(d_2) > 0:
		# create the traverse objects
		key_1, key_2 = next(iter(d_1)), next(iter(d_2))
		# value of interest
		value_1, value_2 = d_1[key_1][1], d_2[key_2][1]
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

def merge_on_transfers(d_1, d_2):
	"""
	This functions merges two dictionaries (each of which are assumed to be sorted as desired)
	"""
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

def merge_sort_time(d_input):
	d_return = copy.deepcopy(d_input)
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
		d_1 = merge_sort_time(d_1)
		d_2 = merge_sort_time(d_2)
		# sorting
		d_return = merge_on_time(d_1, d_2)
	# return
	return d_return

def merge_sort_transfers(d_input):
	d_return = copy.deepcopy(d_input)
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
		d_1 = merge_sort_transfers(d_1)
		d_2 = merge_sort_transfers(d_2)
		# sorting
		d_return = merge_on_transfers(d_1, d_2)
	# return
	return d_return

def end_route_first(d, end_routes_list):
	# create the return object 
	d_return = {}
	d_temp = {}
	# 
	while len(d) > 0:
		journey_id = next(iter(d))
		quadruple = d[journey_id]
		route = quadruple[2]
		if route in end_routes_list:
			d_return[journey_id] = quadruple
		else:
			d_temp[journey_id] = quadruple
		del d[journey_id]

	while len(d_temp) > 0:
		journey_id = next(iter(d_temp))
		quadruple = d_temp[journey_id]
		d_return[journey_id] = quadruple
		del d_temp[journey_id]

	return d_return


def merge_sort(d_input, end_routes_list):
	d_return = merge_sort_time(d_input)
	d_return = merge_sort_transfers(d_return)
	d_return = end_route_first(d_return, end_routes_list)
	return d_return