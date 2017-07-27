# imports
import random
import merge_sort
import pickle

"""
JPI
	Weekday
		Time
			Stop
				CTT
"""



# STOP
# Grid
def grid(x, y):
	# ranges
	x_range = range(0, x, 1)
	y_range = range(0, y, 1)
	stop_id_range = range(0, x * y, 1)
	# coordinates list
	coordinates_list = [(h, v) for h in x_range for v in y_range]
	# stop_id dictionary
	stop_dict = dict()
	for s in stop_id_range:
		stop_dict[s] = coordinates_list[s]
	return [x, y, stop_dict]

def grid_review(grid_output):
	stop_dict = grid_output[2]
	for item in stop_dict:
		print("stop: {}, coordinate: {}".format(item, stop_dict[item]))


# Route
def route(value, row_or_column, grid_output, route_dict, route_id_list):
	# unpack data
	rows = grid_output[0]
	columns = grid_output[1]
	stop_dict = grid_output[2]
	# route_id
	try:
		route_id = route_id_list[-1] + 1
	except:
		route_id = 1
	# instantiate route
	route = dict()
	# instantiate position
	position = 0
	# populate route
	if row_or_column == "row":
		for stop in stop_dict:
			pair = stop_dict[stop]
			row_value = pair[0]
			if row_value == value:
				route[stop] = (pair, position)
				position += 1
	else:
		for stop in stop_dict:
			pair = stop_dict[stop]
			column_value = pair[1]
			if column_value == value:
				route[stop] = (pair, position)
				position += 1
	# add to route_dict
	route_dict[route_id] = route
	# add the reverse_route to route_dict
	reversed_route_id = route_id * -1
	route_dict[reversed_route_id] = merge_sort.merge_sort_for_generation(route)
	# increment the route_id
	route_id_list.append(route_id)

def route_review(route_output):
	print("Routes & Coordinates & Position")
	for route in route_output:
		print("route: {}, stops & coordinates & positions: {}".format(route, route_output[route]))
	print("")


def route_simple(route_dict):
	route_dict_simple = dict()
	for route_id in route_dict:
		stop_dict = route_dict[route_id]
		stop_list = list()
		for stop in stop_dict:
			stop_list.append(stop)
		route_dict_simple[route_id] = stop_list
	return route_dict_simple

def route_simple_review(route_simple_output):
	print("Routes")
	for route in route_simple_output:
		print("route: {}, stops: {}".format(route, route_simple_output[route]))
	print("")



# CTT: assumed output of models
def route_ctt(route_simple_output):
	route_cct_dict = dict()
	for route_id in route_simple_output:
		time = random.randint(1, 10)
		route = route_simple_output[route_id]
		first_entry = route[0]
		temp_dict = dict()
		for stop in route:
			temp_dict[stop] = round(time * random.uniform(1.1, 1.5), 2)
			time = temp_dict[stop]
		temp_dict[first_entry] = 0
		route_cct_dict[route_id] = temp_dict
	return route_cct_dict

def route_ctt_review(route_ctt_output):
	print("Routes & CTT")
	for route in route_ctt_output:
		print("route: {}, stops: {}".format(route, route_ctt_output[route]))
	print("")

def route_ctt_to_file(route_ctt_output):
	destination = open("test_data.p", "wb")
	pickle.dump(route_ctt_output, destination)
	destination.close()



if __name__ == "__main__":
	# create the grid
	grid_output = grid(10, 10)
	route_dict = dict()
	route_id_list = []
	
	route(2, "row", grid_output, route_dict, route_id_list)
	route(2, "column", grid_output, route_dict, route_id_list)
	route(7, "row", grid_output, route_dict, route_id_list)
	# route_review(route_dict)

	route_dict_simple = route_simple(route_dict)
	# route_simple_review(route_dict_simple)
	
	route_ctt_output = route_ctt(route_dict_simple)
	route_ctt_review(route_ctt_output)

	route_ctt_to_file(route_ctt_output)