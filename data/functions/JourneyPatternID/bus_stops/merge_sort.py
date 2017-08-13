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


def merge_dict_who_is_first(d1, d2):
	"""
	This functions merges two dictionaries (each of which are assumed to be sorted as desired)
	"""
	# create the return object 
	d = {}
	# get largest elements until one dict is empty
	while len(d1) > 0 and len(d2) > 0:
		# create the traverse objects
		large_1, large_2 = next(iter(d1)), next(iter(d2))
		# put the higher score into the return dictionary
		if d1[large_1] > d2[large_2]:
			d[large_1] = d1[large_1]
			del d1[large_1]
		else:
			d[large_2] = d2[large_2]
			del d2[large_2]
	# add remaining elements
	while len(d1) > 0:
		large = next(iter(d1))
		d[large] = d1[large]
		del d1[large]
	while len(d2) > 0:
		large = next(iter(d2))
		d[large] = d2[large]
		del d2[large]
	# return
	return d

def merge_sort_dict_who_is_first(d):
	"""
	This is the recursive implementation of merge sort for a specific dictionary generated in neighbours in routes_alternative
	"""
	# objects
	d1 = {}
	d2 = {}
	length = len(d)
	middle = int(length / 2)

	# split the data into two parts
	if len(d) > 1:
		for i in range(0, middle, 1):
			next_item = next(iter(d))
			d1[next_item] = d[next_item]
			del d[next_item]
		for i in range(middle, length, 1):
			next_item = next(iter(d))
			d2[next_item] = d[next_item]
			del d[next_item]
		# recursion
		d1 = merge_sort_dict_who_is_first(d1)
		d2 = merge_sort_dict_who_is_first(d2)
		# sorting
		d = merge_dict_who_is_first(d1, d2)
	# return
	return d




def merge_dict_left_neighbours(d1, d2):
	"""
	This functions merges two dictionaries (each of which are assumed to be sorted as desired)
	"""
	# create the return object 
	d = {}
	# get largest elements until one dict is empty
	while len(d1) > 0 and len(d2) > 0:
		# create the traverse objects
		large_1, large_2 = next(iter(d1)), next(iter(d2))
		# put the higher score into the return dictionary
		if d1[large_1] > d2[large_2]:
			d[large_1] = d1[large_1]
			del d1[large_1]
		else:
			d[large_2] = d2[large_2]
			del d2[large_2]
	# add remaining elements
	while len(d1) > 0:
		large = next(iter(d1))
		d[large] = d1[large]
		del d1[large]
	while len(d2) > 0:
		large = next(iter(d2))
		d[large] = d2[large]
		del d2[large]
	# return
	return d

def merge_sort_dict_left_neighbours(d):
	"""
	This is the recursive implementation of merge sort for a specific dictionary generated in neighbours in routes_alternative
	"""
	# objects
	d1 = {}
	d2 = {}
	length = len(d)
	middle = int(length / 2)

	# split the data into two parts
	if len(d) > 1:
		for i in range(0, middle, 1):
			next_item = next(iter(d))
			d1[next_item] = d[next_item]
			del d[next_item]
		for i in range(middle, length, 1):
			next_item = next(iter(d))
			d2[next_item] = d[next_item]
			del d[next_item]
		# recursion
		d1 = merge_sort_dict_left_neighbours(d1)
		d2 = merge_sort_dict_left_neighbours(d2)
		# sorting
		d = merge_dict_left_neighbours(d1, d2)
	# return
	return d