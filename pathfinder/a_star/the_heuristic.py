# imports



def target_route_goes_first(journies_dict, target_routes):
	# [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "n/a")]]}]
	# data
	first_list = list()
	second_list = list()
	return_dict = dict()
	# iterate over each journey in journies_dict
	for jpi in journies_dict:
		# unpack the data
		value = journies_dict[jpi]
		details = value[1]
		quadruple = details[-1]
		route = quadruple[3]
		# if the journey is on the target route, put it at the front of the line
		if route in target_routes:
			first_list.append(jpi)
		else:
			second_list.append(jpi)
		# populate return_dict
		for jpi in first_list:
			return_dict[jpi] = journies_dict[jpi]
		for jpi in second_list:
			return_dict[jpi] = journies_dict[jpi]
	# return
	return return_dict



def create_target_routes(stop, stop_dict):
	target_routes = set()
	data = stop_dict[stop]
	for quadruple in data:
		target_routes.add(quadruple[3])
	return list(target_routes)