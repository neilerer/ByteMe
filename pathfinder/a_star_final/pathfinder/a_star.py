# imports
import merge_sort



def time_unit_model_dict(weekday, time_unit, model_dict):
	# time_unit_dict
	return model_dict[weekday][time_unit]



def start_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set):
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	if start_stop_id == end_stop_id:
		return [True, {0 :[0.00, [(start_stop_id, end_stop_id, 0.00, None) ], None], }]
	# ending_dict
	ending_dict = journies_dict
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
		journey_id = 0
	# record that we've been to this bus stop
	been_set.add(start_stop_id)
	# find the quadruples associated with potential next stops
	list_of_start_stop_quadruples = time_unit_dict[start_stop_id]
	# populate ending_dict
	for quadruple in list_of_start_stop_quadruples:
		# extract information
		next_stop_id = quadruple[1]
		next_stop_journey_time = quadruple[2]
		next_stop_route = quadruple[3]
		# determine if a journey should be created
		if (next_stop_id not in been_set) and (next_stop_id is not None):
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			ending_dict[journey_id] = [next_stop_journey_time, [quadruple], [next_stop_route]]
			# increment the journey_id
			journey_id += 1
	# sort endin_dict
	ending_dict = merge_sort.merge_sort_journies_dict(ending_dict)
	# return
	return [False, ending_dict]



def continue_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set):
	# time_unit_dict
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	# instantiate continuing_dict
	continuing_dict = journies_dict
	# sort continuing_dict so that the shortest journey is considered
	continuing_dict = merge_sort.merge_sort_journies_dict(continuing_dict)
	# ending_dict
	ending_dict = dict()
	# continue the shortest journey
	for jid in continuing_dict:
		# unpack
		journey_id = jid
		current_journey_time = continuing_dict[jid][0]
		quadruple_list = continuing_dict[jid][1]
		route_list = continuing_dict[jid][2]
		# more unpacking
		current_stop_id = quadruple_list[-1][1]
		# termination condition
		if current_stop_id == end_stop_id:
			return [True, {journey_id : continuing_dict[journey_id]}]
		# evaluate the next stop after current_stop_id
		try:
			list_of_next_stop_quadruples = time_unit_dict[current_stop_id]
		except:
			# return
			if not continuing_dict:
				# create journey_path
				journey_path = list()
				for quadruple in quadruple_list:
					journey_path.append(quadruple)
				journey_path.append("{} is not in model_dict".format(current_stop_id))
				return [True, {journey_id: [None, been_set, journey_path]}]
			else:
				return [False, continuing_dict]
		# iterate over the quadruples
		for quadruple in list_of_next_stop_quadruples:
			# extract information
			next_stop_id = quadruple[1]
			next_stop_journey_time = quadruple[2]
			next_stop_route = quadruple[3]
			# determine if a journey should be created
			if (next_stop_id not in been_set) and (next_stop_id is not None) and ((next_stop_route not in route_list) or (next_stop_route in route_list and next_stop_route == route_list[-1])):
				# create element of new part to add
				current_journey_path = quadruple_list
				# update been_set
				been_set.add(next_stop_id)
				# update route_list
				route_list.append(next_stop_route)
				# create a new journey id
				journey_id = journey_id_list[-1] + 1
				journey_id_list.append(journey_id)
				# create the journey path
				journey_path = list()
				for item in current_journey_path:
					journey_path.append(item)
				journey_path.append(quadruple)
				ending_dict[journey_id] = [current_journey_time + next_stop_journey_time, journey_path, route_list]
	# return
	if not ending_dict:
		# create journey_path
		journey_path = list()
		for quadruple in current_journey_contents[2]:
			journey_path.append(quadruple)
		journey_path.append("There is no bus journey from {} to {} via {}".format(start_stop_id, end_stop_id, path))
		return [True, {journey_id: [None, journey_path]}]
		# return [True, {0: None}]
	else:
		return [False, ending_dict]



def a_star(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set):
	# data objects
	found_shortest_path = False
	# start
	result = start_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
	found_shortest_path = result[0]
	journies_dict = result[1]
	# continue
	while found_shortest_path is False:
		result = continue_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
		found_shortest_path = result[0]
		journies_dict = result[1]
	# return
	shortest_path_details = None
	for journey_id in journies_dict:
		shortest_path_details = journies_dict[journey_id]
	return shortest_path_details



