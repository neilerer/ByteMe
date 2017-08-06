# imports



def user_input(start_stop_id, end_stop_id, weekday, time_unit, model_dict):
	# find the appropriate data
	time_unit_dict = model_dict[weekday][time_unit]
	# get details
	start_details = time_unit_dict[start_stop_id]
	end_details = time_unit_dict[end_stop_id]
	# details (start_stop_id, end_stop_id, journey_time, route_id)
	return [start_details, end_details]



def routes_in_detail(start_or_stop_detail):
	route_list = list()
	for quadruple in start_or_stop_detail:
		route = quadruple[3]
		route_list.append(route)
	return route_list

def path_possibilities(user_input_output):
	# unpack the data
	start_details = user_input_output[0]
	end_details = user_input_output[1]
	# create routes
	start_routes = routes_in_detail(start_details)
	end_routes = routes_in_detail(end_details)
	# create combinations
	route_combinations = list()
	for sr in start_routes:
		for er in end_routes:
			route_combinations.append((sr, er))
	return route_combinations