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
	# calculate the percentages
	for key in neighbours:
		neighbours[key][1] = neighbours[key][0] / total
	# sort neighbours
	neighbours = merge_sort.merge_sort_dict(neighbours)
	# return neighbours
	return neighbours


def stop_id_neighbour_information_basic(routes_weekday_output, unique_stops_output, resident_stop, side):
	rank_array = neighbours(routes_weekday_output, unique_stops_output, resident_stop, side)
	rank = merge_sort.get_first_entry_of_dict(rank_array)[1][1]
	return [resident_stop, side, rank, rank_array]


# def neighbours_pct(routes_weekday_output, unique_stops_output, resident_stop, side):
# 	# create the count of side-neighbours
# 	side_neighbours = neighbours(routes_weekday_output, unique_stops_output, resident_stop, side)
# 	# determine the number of neighbours
# 	total_neighbours = sum(side_neighbours)
# 	# exit if the count is zero
# 	if total_neighbours == 0:
# 		return [0 for x in side_neighbours]
# 	# holding list
# 	neighbours_list = []
# 	# initialise a count and count_bound
# 	count = 0
# 	count_bound = len(side_neighbours)
# 	# iterate over side_neighbours to populate neighbours
# 	while count < count_bound:
# 		neighbours_list.append(side_neighbours[count] / total_neighbours)
# 		count += 1
# 	# return
# 	return neighbours_list

# def neighbours_next_door(routes_weekday_output, unique_stops_output, resident_stop):
# 	left_neighbours = neighbours_pct(routes_weekday_output, unique_stops_output, resident_stop, 'left')
# 	right_neighbours = neighbours_pct(routes_weekday_output, unique_stops_output, resident_stop, 'right')
# 	return [left_neighbours, right_neighbours]


file_name = "00010001.csv"
resident_stop = '226'
side = 'left'
journeys_for_each_weekday = journeys(file_name)
monday_uid_routes_dict = journeys_weekday(journeys_for_each_weekday, 0)
monday_routes = routes_weekday(journeys_for_each_weekday, 0)
stops = unique_stops(monday_routes)
# resident_stop_neighbours = neighbours(monday_routes, stops, resident_stop, side)
stop_id_information_basic = stop_id_neighbour_information_basic(monday_routes, stops, resident_stop, side)

print(stop_id_information_basic)

# both_neighbours = neighbours_next_door(monday_routes, stops, resident_stop)
# for item in both_neighbours:
# 	print(item)


# # generate all neighbours for a weekday route
# def all_weekday_neighbours(routes_weekday_output, unique_stops_output):
# 	# holding list
# 	all_neighbours = []
# 	# iterate over each resident stop
# 	for resident_stop in unique_stops_output:
# 		# create the data
# 		data = neighbours_next_door(routes_weekday_output, unique_stops_output, resident_stop)
# 		# articulate the data
# 		left_neighbours = data[0]
# 		right_neighbours = data[1]
# 		# determine the maximum values
# 		left_max = max(left_neighbours)
# 		right_max = max(right_neighbours)
# 		# append to the neighbour list
# 		all_neighbours.append([resident_stop, left_max, right_max, left_neighbours, right_neighbours])
# 	# return
# 	return all_neighbours

# def find_max_neighbours(all_weekday_neighbours_output):
# 	# 
# 	left_maximum = 0
# 	right_maximum = 0
# 	left_location = 0
# 	right_location = 0
# 	count = 0
# 	for neighbour_list in all_weekday_neighbours_output:
# 		current_left = neighbour_list[1]
# 		current_right = neighbour_list[2]
# 		if current_left > left_maximum:
# 			left_maximum = current_left
# 			left_location = count
# 		if current_right > right_maximum:
# 			right_maximum = current_right
# 			right_location = count
# 		count += 1
# 	if left_maximum > right_maximum:
# 		return all_weekday_neighbours_output[left_location]
# 	else:
# 		return all_weekday_neighbours_output[right_location]



# file_name = "00010001.csv"
# all_weekday_journeys = journeys(file_name)
# weekday = 0
# weekday_routes = routes_weekday(all_weekday_journeys, weekday)
# stops = unique_stops(weekday_routes)
# weekday_neighbours = all_weekday_neighbours(weekday_routes, stops)
# for item in weekday_neighbours:
# 	print(item)
# 	print("")
# maximum = find_max_neighbours(weekday_neighbours)
# print(maximum)