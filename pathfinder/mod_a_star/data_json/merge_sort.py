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



def merge_journies_dict(d_1, d_2):
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

def merge_sort_journies_dict(d_input):
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
		d_1 = merge_sort_journies_dict(d_1)
		d_2 = merge_sort_journies_dict(d_2)
		# sorting
		d_return = merge_journies_dict(d_1, d_2)
	# return
	return d_return



def merge_route_dict(d_1, d_2):
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
		value_1, value_2 = int(key_1), int(key_2)
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

def merge_sort_route(d_input):
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
		d_1 = merge_sort_route(d_1)
		d_2 = merge_sort_route(d_2)
		# sorting
		d_return = merge_route_dict(d_1, d_2)
	# return
	return d_return