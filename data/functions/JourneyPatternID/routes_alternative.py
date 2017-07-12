# imports
import os
import routes
import merge_sort


# fundamental data
def journeys(file_name):
	# list of dictionaries, one for each weekday, where key:value is uid:stops
	return routes.weekday_stops(file_name)

def journeys_weekday(journeys_output, weekday):
	# dictionary: key: value is uid:stops
	return journeys_output[weekday]

def routes_weekday(journeys_output, weekday):
	weekday_journey = journeys_weekday(journeys_output, weekday)
	# list of lists where each list is the stops from a related journey
	return [weekday_journey[key] for key in weekday_journey]


# counting utilities
def unique_stops(routes_weekday_output):
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
	stops = stops + ["left", "right"]
	# return stops
	return stops

def neighbours(routes_weekday_output, unique_stops_output, resident_stop, side):
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
								# neighbours[-1] += 1
								neighbours['right'][0] += 1
							else:
								# find and increment the value in neighbours
								neighbour = stop_list[stop_count + 1]
								# neighbour_index = unique_stops_output.index(neighbour)
								# neighbours[neighbour_index] += 1
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
								# neighbours[-2] += 1
								neighbours['left'][0] += 1
							else:
								# find and increment the value in neighbours
								neighbour = stop_list[stop_count - 1]
								# neighbour_index = unique_stops_output.index(neighbour)
								# neighbours[neighbour_index] += 1
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
		neighbours[key][1] = neighbours[key][0] / total
	# sort neighbours
	neighbours = merge_sort.merge_sort_dict_neighbours(neighbours)
	# return neighbours
	return neighbours


# fundamental unit of route finding algorithm
def stop_id_neighbour_information(routes_weekday_output, unique_stops_output, resident_stop, side):
	rank_array = neighbours(routes_weekday_output, unique_stops_output, resident_stop, side)
	# never has a neighbour array check
	if rank_array == [None]:
		return rank_array
	rank_info = merge_sort.get_first_entry_of_dict(rank_array)[1]
	n = rank_info[0]
	n_rank = rank_info[1]
	# return [StopID, n_side, match_status, n, n_rank, rank_array, key]
	return [resident_stop, side, False, n, n_rank, rank_array, None]

def stop_id_neighbour_information_summary(stop_id_info):
	labels = ["StopID", "Neighbour Side", "Match Status", "Neighbour", "Neighbour Rank", "Neighbour Rank Array", "Solution Key"]
	count = 0
	print("")
	for item in stop_id_info:
		print(labels[count] + ":", item)
		count += 1


# aggregating all stop_id_neighbour_information outputs into an array sorted by neighbour rank
def stop_id_neighbour_information_array(routes_weekday_output, unique_stops_output):
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



file_name = "00010001.csv"
resident_stop = '226'
side = 'left'
journeys_for_each_weekday = journeys(file_name)
monday_uid_routes_dict = journeys_weekday(journeys_for_each_weekday, 0)
monday_routes = routes_weekday(journeys_for_each_weekday, 0)
stops = unique_stops(monday_routes)
# resident_stop_neighbours = neighbours(monday_routes, stops, resident_stop, side)
# stop_id_info = stop_id_neighbour_information(monday_routes, stops, resident_stop, side)
# print("")
# print(stop_id_info)
# print("")
# stop_id_neighbour_information_summary(stop_id_info)
all_stop_id_neighbour_information_array = stop_id_neighbour_information_array(monday_routes, stops)
print(all_stop_id_neighbour_information_array)