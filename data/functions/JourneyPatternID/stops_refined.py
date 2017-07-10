# imports
import os
import stops_raw


"""
These functions transform the raw stop-related JourneyPatternID information into stop lists
Presently they are organised by day of the week and JourneyPatternID
"""


# INITIAL REFINEMENT: STOPS ONLY (NO IDLING)
"""
This generates all the unique ids of the triples for each weekday
This uses the output of journeys
"""
def unique_id_list(weekday_data):
	# data
	list_of_triple_lists = weekday_data[0]
	weekdays = weekday_data[1]
	list_of_unique_ids = []
	# iterate over each weekday
	for wd in weekdays:
		# list that will hold uids for each weekday
		uid_list = []
		# list of triples for a given weekday
		triple_list = list_of_triple_lists[wd]
		# iterate over each triple
		for triple in triple_list:
			# check if the uid is known
			if triple[2] in uid_list:
				# pass if it is
				pass
			else:
				# record otherwise
				uid_list.append(triple[2])
		# append to the list of unique id lists for each week
		list_of_unique_ids.append(uid_list)
	# return
	return list_of_unique_ids

"""
For each weekday, for each uid, we have the journey (including idling at the same stop)
"""
def journeys(file_name):
	# data
	source = stops_raw.weekday_data(file_name)
	stops_list = source[0]
	weekdays = source[1]
	uid_list = unique_id_list(source)
	uid_stop_list = []
	# iterate over the weekdays
	for wd in weekdays:
		# data
		list_of_stops = stops_list[wd]
		list_of_uids = uid_list[wd]
		list_of_uid_stops = [[] for uid in list_of_uids]
		# iterate over the triples
		for triple in list_of_stops:
			# find where it is in the uid list
			index = list_of_uids.index(triple[2])
			# put it into the corresponding position in the uid stop list
			list_of_uid_stops[index].append(triple)
		# append to the list holding similar objects for each weekday
		uid_stop_list.append(list_of_uid_stops)
	# return 
	# - list with seven lists, one for each day:
	# - - a list for each uid showing a (Timestamp, StopID, uid) triple as it traveled in time
	return [uid_stop_list, weekdays]

def unique_journeys(file_name):
	# data
	source = stops_raw.weekday_data(file_name)
	stops_list = source[0]
	weekdays = source[1]
	uid_list = unique_id_list(source)
	uid_stop_list = []
	# iterate over the weekdays
	for wd in weekdays:
		# data
		list_of_stops = stops_list[wd]
		list_of_uids = uid_list[wd]
		list_of_uid_stops = [[] for uid in list_of_uids]
		# iterate over the triples
		for triple in list_of_stops:
			# find where it is in the uid list
			index = list_of_uids.index(triple[2])
			# check if not needed
			try:
				if list_of_uid_stops[index][-1][1] == triple[1]:
					pass
				else:
					# put it into the corresponding position in the uid stop list
					list_of_uid_stops[index].append(triple)
			except:
				# put it into the corresponding position in the uid stop list
				list_of_uid_stops[index].append(triple)
		# append to the list holding similar objects for each weekday
		uid_stop_list.append(list_of_uid_stops)
	# return 
	# - list with seven lists, one for each day:
	# - - a list for each uid showing a (Timestamp, StopID, uid) triple as it traveled in time
	# - - only stops, not idling is recorded
	return [uid_stop_list, weekdays]

def unique_journeys_stop_ids_only(file_name):
	# data
	source = unique_journeys(file_name)
	weekday_uid_triple_list = source[0]
	weekdays = source[1]
	weekday_uid_stop_list = [[] for wd in weekdays]
	# 
	for wd in weekdays:
		weekday_list = weekday_uid_triple_list[wd]
		weekday_stop_list = weekday_uid_stop_list[wd]
		for uid_list in weekday_list:
			if len(uid_list) < 2:
				pass
			else:
				uid_stop_list = []
				for triple in uid_list:
					try:
						if triple[1] in uid_stop_list:
							pass
						else:
							uid_stop_list.append(triple[1])
					except:
						pass
			weekday_stop_list.append(uid_stop_list)
		weekday_uid_stop_list[wd].append(weekday_stop_list)
	return weekday_uid_stop_list


# PAIRWISE COMPARISON OF STOP LISTS: DETAILS OF ITEMS NOT IN PRIMARY_ARRAY BUT IN SECONDARY_ARRAY
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


def route_for_jpi_on_weekday(file_name, weekday):
	# data
	unique_journeys = unique_journeys_stop_ids_only(file_name)
	# preliminary matters
	primary_array = unique_journeys[weekday][0]
	secondary_array = unique_journeys[weekday][1]
	source = pairwise_stop_id_list_length_2(primary_array, secondary_array)
	final_array = source[0]
	details = source[1]
	# iterative calculation of route
	for item in unique_journeys[weekday][1::1]:
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


good_array = unique_journeys_stop_ids_only("00010001.csv")
for item in good_array:
	print(item)

bad_array = unique_journeys_stop_ids_only("00411003.csv")
for item in bad_array:
	print(item)

"""
Below here is where I futz about with the code while in development
"""
# file_name = "00010001reduced.csv"

# uj_data = unique_journeys_stop_ids_only(file_name)
# for i in range(0, 10, 1):
# 	primary_array = uj_data[i][0]
# 	secondary_array = uj_data[i][1]
# 	source = pairwise_stop_id_list_length_2(primary_array, secondary_array)
# 	final_array = source[0]
# 	details = source[1]

# 	for item in uj_data[0][1::1]:
# 		# length 2 issues
# 		source = pairwise_stop_id_list_length_2(final_array, item)
# 		final_array = source[0]
# 		# length 1 issues
# 		source = stop_id_list_length_1_fix(final_array, details)
# 		final_array = source[0]

# 	print("uid", i)
# 	print(final_array)
# 	print("")

# import time
# start = time.time()
# for i in range(0, 7, 1):
# 	data = route_for_jpi_on_weekday(file_name, i)
# 	print("Weekday:", i)
# 	print("Length:", len(data))
# 	print(data)
# 	print("")
# print(time.time() - start)

# c_list = [226, 228, 229, 227, 230, 231, 1641, 1642, 213, 214, 4432, 119, 44, 45, 46,47,48,49,50,51,52,265,271,340,350,351,352,353,354,355,356,357,390,372,373,374,375,380,2804,376, 377, 378]