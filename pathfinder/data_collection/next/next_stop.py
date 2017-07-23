# import
import random
import general
import merge_sort
import source_data



def bus_stops(bus_stop_dict):
	"""
	Purpose
	- generate a list of all the unique bus stops
	
	Input
	- bus_stop_dict
	-- output of source_data.jpi_dictoinary()
	--- creates a dicitonary with key of JPI and value a list of associated bus stops
	
	Output
	- a list of all unique bust stop ids
	
	"""
	# holder for return values
	bus_stop_unique_values = set()
	# iterate over each jpi
	for jpi in bus_stop_dict:
		# check each stop in each jpi
		for stop in bus_stop_dict[jpi]:
			# add to the set we are using to hold unique values
			bus_stop_unique_values.add(stop)
	# return
	return list(bus_stop_unique_values)



# TEMPORARY RANDOM TIME VALUE GENERATOR; WILL BE REPLACED BY SYNCING UP MODEL DATA IN THE FUTURE
def random_journey_time():
	return random.randint(1, 11)



def next_for_stop_id(stop_id, bus_stop_dict):
	"""
	Purpose
	- generate a tuple (stop id, {(next stop id, next stop id jpi): False, ...})
	- intended to be used in a function that generates a similar tuple for each stop id

	Input
	- stop_id
	-- a bus stop id
	- bus_stop_dict
	-- output of source_data.jpi_dictoinary()
	--- creates a dicitonary with key of JPI and value a list of associated bus stops

	Output
	- a tuple (stop id, {(next stop id, next stop id jpi): False, ...})

	"""

	next_dict = {}
	for jpi in bus_stop_dict:
		try:
			index = bus_stop_dict[jpi].index(stop_id) + 1
			key = (bus_stop_dict[jpi][index], jpi)
			next_dict[key] = random_journey_time()
		except:
			pass
	next_dict = merge_sort.merge_sort_next_for_stop_id(next_dict)
	return (stop_id, next_dict)



def next_for_all():
	"""
	Purpose
	- use next_for_stop_id() on on all stop ids to return a dictionary
	-- key: stop_id
	-- value: the dictionary element of next_for_stop_id()

	Input
	- None

	Output
	- a dictionary
	-- key: stop_id
	-- value: the dictionary element of next_for_stop_id()
	--- {(next stop id, next stop id jpi): False, ...}

	"""

	# generate the source data
	bus_stop_dict = source_data.jpi_dictionary()
	# instantiate the return object
	next_dict = {}
	# generate the list of unique bus stops
	bus_stop_unique_values = bus_stops(bus_stop_dict)
	# iterate over the unique bus stops
	for stop_id in bus_stop_unique_values:
		# generate the data for that stop id
		data = next_for_stop_id(stop_id, bus_stop_dict)
		# set the stop id as the key and the dictionary from next_for_stop_id() as the value
		next_dict[data[0]] = data[1]
	# return the dictionary
	return next_dict



if __name__ == "__main__":
	my_dict = next_for_all()
	for item in my_dict:
		print(item)
		print(my_dict[item])
		print("")