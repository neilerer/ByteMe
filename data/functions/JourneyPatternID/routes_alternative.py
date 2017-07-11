# imports
import os
import routes


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
	neighbours = [0 for stop in unique_stops_output]
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
								neighbours[-1] += 1
							else:
								# find and increment the value in neighbours
								neighbour = stop_list[stop_count + 1]
								neighbour_index = unique_stops_output.index(neighbour)
								neighbours[neighbour_index] += 1
						except:
							pass
					else:
						try:
							# check if the observation is the left-most element of the list
							if stop_count == 0:
								# increment the left counter in neighbours
								neighbours[-2] += 1
							else:
								# find and increment the value in neighbours
								neighbour = stop_list[stop_count - 1]
								neighbour_index = unique_stops_output.index(neighbour)
								neighbours[neighbour_index] += 1
						except:
							pass
				# increment the counter
				stop_count += 1
	# return neighbours
	return neighbours

def neighbours_pct(routes_weekday_output, unique_stops_output, resident_stop, side):
	# create the count of side-neighbours
	side_neighbours = neighbours(routes_weekday_output, unique_stops_output, resident_stop, side)
	# determine the number of neighbours
	total_neighbours = sum(side_neighbours)
	# holding list
	neighbours_list = []
	# initialise a count and count_bound
	count = 0
	count_bound = len(side_neighbours)
	# iterate over side_neighbours to populate neighbours
	while count < count_bound:
		neighbours_list.append(side_neighbours[count] / total_neighbours)
		count += 1
	# return
	return neighbours_list

def neighbours_next_door(routes_weekday_output, unique_stops_output, resident_stop):
	left_neighbours = neighbours_pct(routes_weekday_output, unique_stops_output, resident_stop, 'left')
	right_neighbours = neighbours_pct(routes_weekday_output, unique_stops_output, resident_stop, 'right')
	return [left_neighbours, right_neighbours]



file_name = "00010001.csv"
resident_stop = '226'
data = journeys(file_name)
monday = journeys_weekday(data, 0)
monday_routes = routes_weekday(data, 0)
stops = unique_stops(monday_routes)
both_neighbours = neighbours_next_door(monday_routes, stops, resident_stop)
for item in both_neighbours:
	print(item)