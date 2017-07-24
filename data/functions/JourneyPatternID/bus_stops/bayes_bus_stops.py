# imports
import os
import general
import merge_sort
import generate_routes



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



def left_neighbour(stop_id, route):
	try:
		index = route.index(stop_id)
		if index == 0:
			return 'start'
		else:
			return route[index - 1]
	except:
		return None

def left_neighbours(stop_id, the_routes):
	# return object
	left_dict = {}
	# occurances
	occurances = 0
	# collect and tabulate the number of occurances of the left neighbour
	for route in the_routes:
		neighbour = left_neighbour(stop_id, the_routes[route])
		occurances += 1
		if neighbour is not None:
			if neighbour in left_dict:
				left_dict[neighbour] += 1
			else:
				left_dict[neighbour] = 1
	# convert left_dict values to percentages of total appearances
	for neighbour in left_dict:
		left_dict[neighbour] = left_dict[neighbour] / occurances
	# sort the diciontary
	left_dict = merge_sort.merge_sort_dict_left_neighbours(left_dict)
	# return
	return left_dict

def left_neighbours_dict(the_routes, all_stops):
	neighbours_dict = {}
	for stop in all_stops:
		neighbours_dict[stop] = left_neighbours(stop, the_routes)
	return neighbours_dict

def find_right_neighbour(stop_id, neighbours_dict):
	start = False
	start_value = 0
	for stop in neighbours_dict:
		value_dict = neighbours_dict[stop]
		temp = merge_sort.get_first_entry_of_dict(value_dict)
		if temp[0] == stop_id and temp[1] > start_value:
			start = stop
			start_value = temp[1]
	return start





if __name__ == "__main__":
	the_routes = generate_routes.routes("00010001.csv")
	all_stops = unique_stops(the_routes)
	my_dict = left_neighbours_dict(the_routes, all_stops)
	# for item in my_dict:
	# 	print(item)
	# 	print(my_dict[item])
	# 	print("")
	print(find_right_neighbour("start", my_dict))