# imports
import os
import routes
import merge_sort


# SOURCE DATA
"""
These functions get generate the stops on a JourneyPatternID for each day of the week
"""
def remove_single_values(wd_dict):
	"""
	Purpose
	- used to remove key:value pairs in which the value list has only one element (not useful in imputing route)
	- used withing journeys()
	Inputs
	- wd_dict: dictionary for a given weekday containing key:value of VJID_VID:[StopID list]
	- generated within journeys()
	Outputs
	- None
	- this function modifes the dictionary in place
	"""
	kill_list = []
	# iterate over dictionary keys
	for key in wd_dict:
		# if the associated list has only one element
		if len(wd_dict[key]) == 1:
			# mark this dictionary entry for deletion
			kill_list.append(key)
	# iterate over the keys in kill_list
	for item in kill_list:
		# delete that entry from the dictionary
		del wd_dict[item]

def routes(file_name):
	"""
	Purpose
	- extracts all journeys on a JourneyPatternID
	-- list of seven dictionaries, one for each day of the week
	-- dictionary key:value of VJID_VID:[StopID list]
	Input
	- name of the file containing the information
	- stored in the data/JourneyPatternID directory
	Output
	- a list of seven dictionaries, one for each day of the week
	- dictionary key:value of VJID_VID:[StopID list]
	- only records a bus stop, not an idle i.e each StopID is recorded only if the prior stop was not the same
	"""
	# change directories
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# open the source
	with open(file_name, "r") as source:
		# header
		header = source.readline().strip().split(",")
		# index
		index_wd = header.index("WeekDay")
		index_vjid = header.index("VehicleJourneyID")
		index_vid = header.index("VehicleID")
		index_sid = header.index("StopID")
		# weekday lists
		weekday_dicts = [{} for i in range(0, 7, 1)]
		# iterate over the source document
		for line in source:
			# turn line into list
			line_list = line.strip().split(",")
			try:
				# values
				wd = int(line_list[index_wd])
				vjid = line_list[index_vjid]
				vid = line_list[index_vid]
				uid = vjid + "_" + vid
				# data objects
				uid_dict = weekday_dicts[wd]
				stop_id = line_list[index_sid]
				# if the uid is in the dictionary
				if uid in uid_dict:
					# specify the list that is the value to the uid's key
					stop_list = uid_dict[uid]
					# if the stop_id is different from the last element in the stop_list
					if stop_list[-1] != stop_id:
						# add it to the array
						stop_list.append(stop_id)
				else:
					# create the dictionary
					uid_dict[uid] = [stop_id]
			except:
				pass
		# return to the starting directory
		os.chdir("../../")
		os.chdir("functions/JourneyPatternID")
		# remove elements with just one entry
		for i in range(0, 7, 1):
			wd_dict = weekday_dicts[i]
			remove_single_values(wd_dict)
		# return
		return weekday_dicts

def routes_weekday_dict(routes_output, weekday):
	"""
	Purpose
	- returns a dictionary, representing all journeys on a JourneyPatternID for a given weekday
	- taken from the output of journeys()
	Input
	- journeys_output: the out put of journeys()
	- weekday: an integer in [0:6] representing [M, T, W, R, F, S U]
	Output
	-- dictionary key:value of VJID_VID:[StopID list]
	-- all journeys on a JourneyPatternID for a given weekday
	"""
	return routes_output[weekday]

def routes_weekday_list(routes_output, weekday):
	"""
	Purpose
	- a list of lists, each of which is a journey for a given weekday on a JourneyPatternID
	Input
	- journeys_output: the out put of journeys()
	- weekday: an integer in [0:6] representing [M, T, W, R, F, S U]
	Output
	- a list of lists
	- each list is a unique journey on a JourneyPatternID for a given weekday
	"""
	weekday_route = routes_weekday_dict(routes_output, weekday)
	# list of lists where each list is the stops from a related journey
	return [weekday_route[key] for key in weekday_route]

def unique_stops(specific_weekday_routes):
	# list of stops
	stops = []
	# iterate over the lists
	for stop_list in specific_weekday_routes:
		# iterate over the elements in the list
		for stop in stop_list:
			# check for inclusion
			if stop not in stops:
				# add if not already there
				stops.append(stop)
	# return stops
	return stops


# FIRST STOP BASED METHOD OF DETERMINING ROUTE ORDER
# of the times it occurs, how often is it first
def pct_first(stop_id, specific_weekday_routes, position):
	occurances = 0
	first = 0
	for route in specific_weekday_routes:
		try:
			index = route.index(stop_id)
			occurances += 1
			if index == position:
				first += 1
		except:
			pass
	try:
		return (first / occurances) * first
	except:
		return 0

def who_is_first(all_stops, specific_weekday_routes, position):
	stop_dict = {stop:False for stop in all_stops}
	for stop in all_stops:
		stop_dict[stop] = pct_first(stop, specific_weekday_routes, position)
	stop_dict = merge_sort.merge_sort_dict_who_is_first(stop_dict)
	return stop_dict

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

def bus_stops(all_stops, specific_weekday_routes):
	# data
	unique_stops = all_stops
	weekday_routes = specific_weekday_routes
	# termination condition
	termination_length = len(unique_stops)
	# return object
	bus_stop_list = []
	# loop utnil termination condition is achieved
	while len(bus_stop_list) < termination_length:
		# make the sorted dictionary of stops
		stop_dict = who_is_first(unique_stops, weekday_routes, 0)
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
		unique_stops.pop(unique_stops.index(stop))
		# remove stop from weekday_routes (we will no longer consdier it)
		wr_length = len(weekday_routes)
		for i in range(0, wr_length, 1):
			weekday_routes[i] = remove_element_from_list(stop, weekday_routes[i])
	# return
	return bus_stop_list

def bus_stops_for_jpi(file_name):
	bus_stops_by_weekday = []
	all_weekday_routes = routes(file_name)
	for i in range(0, 7, 1):
		specific_weekday_routes = routes_weekday_list(all_weekday_routes, i)
		all_stops = unique_stops(specific_weekday_routes)
		bus_stops_by_weekday.append(bus_stops(all_stops, specific_weekday_routes))
	return bus_stops_by_weekday

def bus_stop_for_jpi_display(file_name):
	bus_stops = bus_stops_for_jpi(file_name)
	day_dict = {0:"Monday", 1:"Tuesday", 2:"Wednesday", 3:"Thursday", 4:"Friday", 5:"Saturday", 6:"Sunday"}
	name = file_name.split(".")[0]
	print("")
	print("")
	print("Bus Route for JourneyPatternID", name)
	print("")
	for i in range(0, 7, 1):
		print(day_dict[i])
		print(bus_stops[i])
		print("")

bus_stop_for_jpi_display("00010001.csv")