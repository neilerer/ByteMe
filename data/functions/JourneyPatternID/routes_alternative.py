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

def journeys(file_name):
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

def journeys_weekday(journeys_output, weekday):
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
	return journeys_output[weekday]

def routes_weekday(journeys_output, weekday):
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
	weekday_journey = journeys_weekday(journeys_output, weekday)
	# list of lists where each list is the stops from a related journey
	return [weekday_journey[key] for key in weekday_journey]


# PRELIMINARY COLLECTION OF UNIT-LEVEL DATA
"""
These functions draw on the Source Data and create the preliminary unit-level data
"""
def unique_stops(routes_weekday_output):
	"""
	Purpose
	- to generate an array of all unique values of stop
	Input
	- routes_weekday_output: 
	-- a list of lists
	-- each list is a unique journey on a JourneyPatternID for a given weekday
	Output
	- an array containing the unique values of StopIDs for a JourneyPatternID
	"""
	# list of stops
	stops = []
	# iterate over the lists
	for stop_list in routes_weekday_output:
		# iterate over the elements in the list
		for stop in stop_list:
			# check for inclusion
			if stop not in stops:
				# add if not already there
				stops.append(stop)
	# add left and right
	stops = stops + ["start", "end"]
	# return stops
	return stops

def neighbours(routes_weekday_output, unique_stops_output, resident_stop, side):
	"""
	Purpose
	- to generate a a dictionary recording how often each StopID is the side-neighbour of a given StopID
	Input
	- routes_weekday_output: 
	-- a list of lists
	-- each list is a unique journey on a JourneyPatternID for a given weekday
	- unique_stops_output
	-- an array containing the unique values of StopIDs for a JourneyPatternID
	- resident_stop
	-- StopID of interest
	- side
	-- which side-neighbour, "left" or "right", we care about
	Output
	- a dictionary
	- {StopID:[x, y] for StopID in unique_stops_output}
	-- x is how often StopID was the side-neighbour
	-- y is x / sum of all x's, which is the weighted occurance as neighbour
	"""
	# count of how often a unique stop value is a side-neighbour
	neighbours = {uso:[0, 0.0] for uso in unique_stops_output}
	# total to keep track of total occurances of neighbours
	total = 0
	# iterate over each list of stops
	for stop_list in routes_weekday_output:
		# initialise a count and bound
		stop_count = 0
		stop_bound = len(stop_list)
		# if the list has only one entry, it has no neighbours
		if stop_bound == 1:
			pass
		else:
			# iterate over the stops in the stop list
			for stop in stop_list:
				# if you find the resident stop
				if stop == resident_stop:
					if side == "right":
						try:
							# check if the observation is the right-most element of the list
							if stop_count == stop_bound - 1:
								# increase the right counter in neighbours
								neighbours['end'][0] += 1
							else:
								# find and increment the value in neighbours
								neighbour = stop_list[stop_count + 1]
								neighbours[neighbour][0] += 1
							# increment total
							total += 1
						except:
							pass
					else:
						try:
							# check if the observation is the left-most element of the list
							if stop_count == 0:
								# increment the left counter in neighbours
								neighbours['start'][0] += 1
							else:
								# find and increment the value in neighbours
								neighbour = stop_list[stop_count - 1]
								neighbours[neighbour][0] += 1
							# increment total
							total += 1
						except:
							pass
				# increment the counter
				stop_count += 1
	# never has a neighbour check
	if total == 0:
		return [None]
	# calculate the percentages
	for key in neighbours:
		neighbours[key][1] = (neighbours[key][0] / total) * neighbours[key][0]
	# sort neighbours
	neighbours = merge_sort.merge_sort_dict_neighbours(neighbours)
	# return neighbours
	return neighbours


# FUNDAMENTAL UNIT OF THE ROUTE FINDING ALGORITHM
"""
These functions transform the preliminary unit-data into the unit datapoints for the route finding algorithm
"""
def stop_id_neighbour_information(routes_weekday_output, unique_stops_output, resident_stop, side):
	"""
	Purpose
	- generate a seven element list that forms the unit datapoint of the route finding algorithm
	Input
	- routes_weekday_output: 
	-- a list of lists
	-- each list is a unique journey on a JourneyPatternID for a given weekday
	- unique_stops_output
	-- an array containing the unique values of StopIDs for a JourneyPatternID
	- resident_stop
	-- StopID of interest
	- side
	-- which side-neighbour, "left" or "right", we care about
	Output
	- [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
	-- StopID
	-- Neighbour_Side
	--- "left" or "right", indicating which neighbour we care about
	-- Match_Status
	--- True or False, indicating whether or not Neighbour is indicative or assigned
	-- Neighbour
	--- the StopID of the with the highest Neighbour_Rank
	-- Neighbour_Rank
	--- x / y
	---- x is how often Neighbour was the side-neighbour to StopID
	---- y is the total number of time StopID had a side-neighbour
	-- Rank_Array
	--- a sorted dictionary of Potential_Neighbour:[x, y] for each Potential_Neighbour of StopID
	--- Neighbour_Rank is the highest value of y in Rank_Array and Neighbour is the assocaited Potentail Neighbour
	-- Route_Key
	--- None or x in [0,n] for n some integer
	--- indicates which list in Route StopID is located
	"""
	rank_array = neighbours(routes_weekday_output, unique_stops_output, resident_stop, side)
	# never has a neighbour array check
	if rank_array == [None]:
		return rank_array
	rank_info = merge_sort.get_first_entry_of_dict(rank_array)
	n = rank_info[0]
	n_rank = rank_info[1][1]
	# return [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
	return [resident_stop, side, False, n, n_rank, rank_array, None]

def stop_id_neighbour_information_summary(stop_id_info):
	"""
	Purpose
	- to present the result of stop_id_neighbour_information() in human readable format
	Input
	- the output of stop_id_neighbour_information()
	- [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
	Output
	- a vertically oriented represenation of stop_id_neighbour_information() output with labels
	"""
	labels = ["StopID", "Neighbour Side", "Match Status", "Neighbour", "Neighbour Rank", "Neighbour Rank Array", "Solution Key"]
	count = 0
	print("")
	for item in stop_id_info:
		print(labels[count] + ":", item)
		count += 1


# CREATING THE DATA TO BE MANIPULATED TO DETERMINE THE ROUTE
"""
These functions aggregate all stop_id_neighbour_information outputs into an array sorted by Neighbour_Rank, using functions from merge_sort
"""
def stop_id_neighbour_information_array(routes_weekday_output, unique_stops_output):
	"""
	Purpose
	- create an array of stop_id_neighbour_informaiton outputs and sort them by Neighbour_Rank
	Input
	- routes_weekday_output
	-- a list of lists
	-- each list is a unique journey on a JourneyPatternID for a given weekday
	- unique_stops_output
	-- an array containing the unique values of StopIDs for a JourneyPatternID
	Output
	- an array of stop_id_neighbour_informaiton outputs and sort them by Neighbour_Rank
	--[ [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key], . . . ]
	"""
	# array to hold stop_id_neighbour_information output
	array_holder = []
	# iterate to generate all stop_id_neighbour_information output result
	for resident_stop in unique_stops_output:
		for side in ["left", "right"]:
			stop_id_info = stop_id_neighbour_information(routes_weekday_output, unique_stops_output, resident_stop, side)
			# never has a neighbour check
			if stop_id_info == [None]:
				pass
			else:
				array_holder.append(stop_id_info)
	# sort array_holder
	array_holder = merge_sort.merge_sort_array_stop_id_neighbour_information(array_holder)
	# return
	return array_holder

def stop_id_neighbour_information_array_summary(array_holder):
	"""
	Purpose
	- to present the result of stop_id_neighbour_information_array() in human readable format
	Input
	- stop_id_neighbour_informatino_array_ output
	-[ [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key], . . . ]
	Output
	- a vertically oriented represenation of stop_id_neighbour_information() output with labels for each element of stop_id_neighbour_information_array()
	"""
	for item in array_holder:
		stop_id_neighbour_information_summary(item)


# MATCHING AND MODIFICAIONS
"""
These functions match and modify the output of stop_id_neighbour_information() in the process of creating the Route
"""
def match_index(stop_id_neighbour_information_output, array_holder, match_type):
	"""
	Purpose
	- to find the matching element of stop_id_neighbour_information_array()
	Input
	- stop_id_neighbour_information_output
	-- the element we hope to match
	-- [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
	- array_holder
	-- output of stop_id_neighbour_information_array()
	- match_type
	-- what we hope to match with
	--- neighbour: to find Neighbour for the StopID and given Neighbour_Side
	--- other_side: to find the informaiton for the other side of the StopID e.g. left instead of right
	Output
	- if found in the array_holder, the index of the matching set of information
	- if not found in the array holder, and indication of if the desired set of information means the current StopID is either the start or the end of the Route
	"""
	# StopID
	match_stop_id_dict = {"neighbour":3, "other_side":0}
	match_stop_id_index = match_stop_id_dict[match_type]
	match_stop_id = stop_id_neighbour_information_output[match_stop_id_index]
	# n_side
	match_side_dict = {"other_side_left":"right", "other_side_right":"left", "neighbour_left":"left", "neighbour_right":"right"}
	match_side = match_side_dict[match_type + "_" + stop_id_neighbour_information_output[1]]
	# match index
	match_index = 0
	for item in array_holder:
		# define variables for compare
		item_stop_id = item[0]
		item_side = item[1]
		# determine if there is a match
		if item_stop_id == match_stop_id and item_side == match_side:
			# return index of the match
			return match_index
		# increment match_index
		match_index += 1
	# this means it is the beginning (if side was left) or end (if side was right)
	end_type_dict = {"left":"start", "right":"end"}
	return end_type_dict[match_side]

def check_match_status(stop_id_neighbour_information_output):
	"""
	Purpose
	- determine if a given output for stop_id_neighbour_information() is already matched
	Input
	- stop_id_neighbour_information
	- [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
	Output
	- True or False, depending on the value of Match_Status
	"""
	return n[2]

def change_neighbour(stop_id_neighbour_information_output):
	"""
	Purpose
	- change the Neighbour of the StopID (would do if the information for Neighbour indicates it's already matched)
	Input
	- stop_id_neighbour_information
	- [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
	Output
	- an updated stop_id_neighbour_information
	- Rank_Array has removed the original Neighbour entry
	- Neighbour and Neighbour_Rank and the now-highest Neighbour_Rank values
	"""
	# rank array
	rank_array = stop_id_neighbour_information_output[5]
	# remove the already matched neighbour from rank_array
	merge_sort.remove_first_entry_of_dict(rank_array)
	stop_id_neighbour_information_output[5] = rank_array
	# change the neighbour
	new_neighbour_details = merge_sort.get_first_entry_of_dict(rank_array)
	stop_id_neighbour_information_output[3] = new_neighbour_details[0]
	stop_id_neighbour_information_output[4] = new_neighbour_details[1][1]
	# return
	return stop_id_neighbour_information_output


# ROUTE

def 

# source information
file_name = "00010001.csv"
route_journeys = journeys(file_name)
weekday_routes = routes_weekday(route_journeys, 0)
weekday_stops = unique_stops(weekday_routes)
array_holder = stop_id_neighbour_information_array(weekday_routes, weekday_stops)
weekday_route = []
count = 0
count_bound = len(array_holder)
output = {"start":[], "end":[]}
output_index = 0
# matching and modification
while count < count_bound:
	# identify the primary object
	stop_id_info = array_holder[count]
	# check if already matched
	if check_match_status(stop_id_info):
		# increment the count
		count += 1
		# continue the while loop
		continue
	else:
		# find the neighbour
		neighbour_index = match_index(stop_id_info, array_holder, "neighbour")
		# check if edge case
		if neighbour_index is in ["start", "end"]:
			output[neighbour_index].append()

			

			if neighbour_index == "start":
				start_holder.append(neighbour_index)
			else:
				end_holder.append(neighbour_index)
			# increment the count
			count += 1
			# continue the while loop
			continue
		else:
			# get the neighbours information
			neighour_info = array_holder[neighbour_index]
			# check if paired with a match
			if check_match_status(neighour_info):
				# identify where in the array_holder this info resides
				stop_id_info_index = array_holder.index(stop_id_info)
				# modify stop_id_info to get the appropriate neighbour
				stop_id_info = change_neighbour(stop_id_info)
				# update the stop_id_info entry in array_holder
				array_holder[stop_id_info_index] = stop_id_info
				# resort array holder
				array_holder = merge_sort.merge_sort_array_stop_id_neighbour_information(array_holder)
				# start the while loop from the beginning
				count = 0
				continue
			else:
				# [StopID, Neighbour_Side, Match_Status, Neighbour, Neighbour_Rank, Rank_Array, Output_Key]
				# stop_id_info
				stop_id_info[2] = True
				stop_id_info[6] = output_count
				output_count += 1
				output[stop_id_info[6]] = 





	




file_name = "00010001.csv"
resident_stop = '226'
side = 'left'
journeys_for_each_weekday = journeys(file_name)
monday_uid_routes_dict = journeys_weekday(journeys_for_each_weekday, 0)
monday_routes = routes_weekday(journeys_for_each_weekday, 0)
stops = unique_stops(monday_routes)
# resident_stop_neighbours = neighbours(monday_routes, stops, resident_stop, side)
stop_id_info = stop_id_neighbour_information(monday_routes, stops, resident_stop, side)
# print("")
# print(stop_id_info)
# print("")
# stop_id_neighbour_information_summary(stop_id_info)
all_stop_id_neighbour_information_array = stop_id_neighbour_information_array(monday_routes, stops)
# stop_id_neighbour_information_array_summary(all_stop_id_neighbour_information_array)

print(match_index(stop_id_info, all_stop_id_neighbour_information_array, "neighbour"))