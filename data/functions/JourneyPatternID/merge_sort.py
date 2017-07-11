# imports

"""
Implementing a merge sort algorithm for neighbours in routes_alternative
"""

def merge_dict(d1, d2):

	# create the return object 
	d = {}

	# get smallest elements until one dict is empty
	while len(d1) > 0 and len(d2) > 0:

		# create the traverse objects
		d1_small, d2_small = next(iter(d1)), next(iter(d2))

		# put the highest score into the return dictionary
		if d1[d1_small][1] > d2[d2_small][1]:
			d[d1_small] = d1[d1_small]
			del d1[d1_small]
		else:
			d[d2_small] = d2[d2_small]
			del d2[d2_small]

	# add remaining elements
	while len(d1) > 0:
		d1_small = next(iter(d1))
		d[d1_small] = d1[d1_small]
		del d1[d1_small]
	while len(d2) > 0:
		d2_small = next(iter(d2))
		d[d2_small] = d2[d2_small]
		del d2[d2_small]

	# return
	return d

def merge_sort_dict(d):

	# objects
	d1 = {}
	d2 = {}
	length = len(d)
	middle = int(length / 2)

	if len(d) > 1:
		for i in range(0, middle, 1):
			next_item = next(iter(d))
			d1[next_item] = d[next_item]
			del d[next_item]

		for i in range(middle, length, 1):
			next_item = next(iter(d))
			d2[next_item] = d[next_item]
			del d[next_item]

		d1 = merge_sort_dict(d1)
		d2 = merge_sort_dict(d2)
		d = merge_dict(d1, d2)
	
	return d


def remove_first_entry_of_dict(d):
	return d.pop(next(iter(d)))

def get_first_entry_of_dict(d):
	key = next(iter(d))
	value = d[key]
	return [key, value]

neighbours = {'226': [0, 0.0], '228': [7, 0.025362318840579712], '229': [7, 0.025362318840579712], '227': [1, 0.0036231884057971015], '230': [0, 0.0], '231': [1, 0.0036231884057971015], '1641': [0, 0.0], '1642': [0, 0.0], '213': [0, 0.0], '214': [0, 0.0], '4432': [0, 0.0], '119': [0, 0.0], '44': [0, 0.0], '45': [0, 0.0], '46': [0, 0.0], '47': [0, 0.0], '48': [0, 0.0], '49': [0, 0.0], '50': [0, 0.0], '51': [0, 0.0], '52': [0, 0.0], '265': [0, 0.0], '271': [0, 0.0], '340': [0, 0.0], '350': [0, 0.0], '351': [0, 0.0], '352': [0, 0.0], '353': [0, 0.0], '354': [0, 0.0], '355': [0, 0.0], '356': [0, 0.0], '357': [0, 0.0], '390': [0, 0.0], '372': [0, 0.0], '373': [0, 0.0], '374': [0, 0.0], '375': [0, 0.0], '2804': [0, 0.0], '376': [0, 0.0], '378': [4, 0.014492753623188406], '380': [36, 0.13043478260869565], '377': [0, 0.0], '381': [0, 0.0], '385': [0, 0.0], '225': [0, 0.0], 'left': [220, 0.7971014492753623], 'right': [0, 0.0]}
neighbours_ordered = merge_sort_dict(neighbours)
print("")
print(neighbours_ordered)
print("")
print(get_first_entry_of_dict(neighbours_ordered))