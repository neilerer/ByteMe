# imports
import os
import bus_stops_general as general
import bus_stops_merge_sort as merge_sort
import stop_1_routes


# uniqute values of StopID
def unique_stops(routes):
	# list of stops
	stops = []
	# iterate over the lists
	for stop_list in routes:
		# iterate over the elements in the list
		for stop in routes[stop_list]:
			# check for inclusion
			if stop not in stops:
				# add if not already there
				stops.append(stop)
	# return stops
	return stops

the_routes = stop_1_routes.routes("00010001.csv")
all_stops = unique_stops(the_routes)


# of the times it occurs, how often is it first
def pct_first(stop_id, routes, position):
	"""
	Purpose
	- to determine the weighted occurances of a stop_id on a jpi for a given weekday
	Inputs
	- stop_id
	- specific_weekday_routes
	-- output of routes_weekday_list()
	- position
	-- position we care about
	Outputs
	- a floating number greater than or equal to 0
	"""
	# count the number of times the stop_id occurs
	occurances = 0
	# count the number of times the stop_id occurs in position
	pos = 0
	# iterate over the routes
	for route in routes:
		try:
			# find the index; stop_id will occur only once in each route
			index = routes[route].index(stop_id)
			# increment occurances
			occurances += 1
			# if its in the position
			if index == position:
				# increment pos
				pos += 1
		except:
			# if stop_id isn't in the route
			pass
	try:
		# return the weighted occurances of stop_id
		return (pos / occurances) * pos
	except:
		# return zero if stop_id never occurred
		return 0

all_stops = unique_stops(the_routes)
for item in the_routes:
	print(the_routes[item])
print("")
for stop in all_stops:
	print("{}: {}".format(stop, pct_first(stop, the_routes, 0)))


def who_is_first(all_stops, routes, position):
	# dictionary of 
	stop_dict = {stop:False for stop in all_stops}
	for stop in all_stops:
		stop_dict[stop] = pct_first(stop, routes, position)
	stop_dict = merge_sort.merge_sort_dict_who_is_first(stop_dict)
	return stop_dict


print(who_is_first(all_stops, the_routes, 0))