# imports
import merge_sort



def time_unit_model_dict(weekday, time_unit, model_dict):
	# time_unit_dict
	return model_dict[weekday][time_unit]



def start_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict):
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	if start_stop_id == end_stop_id:
		return [True, {0 :[0.00, None, [(start_stop_id, end_stop_id, 0.00, None) ] ] } ]
	# ending_dict
	ending_dict = journies_dict
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
		journey_id = 0
	# record that we've been to this bus stop
	been_set = {start_stop_id}
	# find the quadruples associated with potential next stops
	list_of_start_stop_quadruples = time_unit_dict[start_stop_id]
	# populate ending_dict
	for quadruple in list_of_start_stop_quadruples:
		# extract information
		next_stop_id = quadruple[1]
		next_stop_journey_time = quadruple[2]
		next_stop_route = quadruple[3]
		# determine if a journey should be created
		if (next_stop_id not in been_set) and (next_stop_route in path):
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			ending_dict[journey_id] = [next_stop_journey_time, been_set, [quadruple]]
			# increment the journey_id
			journey_id += 1
	# return
	return [False, ending_dict]



def continue_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict):
	# time_unit_dict
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	# instantiate continuing_dict
	continuing_dict = journies_dict
	# sort continuing_dict so that the shortest journey is considered
	continuing_dict = merge_sort.merge_sort_journies_dict(continuing_dict)
	# continue the shortest journey
	current_journey = merge_sort.remove_first_entry_of_dict(continuing_dict)
	# unpack current_journey
	journey_id = current_journey[0]
	current_journey_contents = current_journey[1]
	current_journey_time = current_journey_contents[0]
	been_set = current_journey_contents[1]
	current_stop_id = current_journey_contents[2][-1][1]
	# evaluate the next stop after current_stop_id
	list_of_next_stop_quadruples = time_unit_dict[current_stop_id]
	# iterate over the quadruples
	for quadruple in list_of_next_stop_quadruples:
		# extract information
		next_stop_id = quadruple[1]
		next_stop_journey_time = quadruple[2]
		next_stop_route = quadruple[3]
		# determine if a journey should be created
		if (next_stop_id not in been_set) and (next_stop_route in path):
			# create element of new part to add
			current_journey_path = current_journey_contents[2]
			# update been_set
			been_set.add(next_stop_id)
			# note journey_id_to_delete
			journey_id_to_delete = journey_id
			# create a new journey id
			journey_id = journey_id_list[-1] + 1
			journey_id_list.append(journey_id)
			# create the journey path
			journey_path = list()
			for item in current_journey_path:
				journey_path.append(item)
			journey_path.append(quadruple)
			continuing_dict[journey_id] = [current_journey_time + next_stop_journey_time, been_set, journey_path]
	# return
	if not continuing_dict:
		return [True, {0: None}]
	else:
		return [False, continuing_dict]



def find_shortest_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict):
	# data objects
	found_shortest_path = False
	# start
	result = start_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
	found_shortest_path = result[0]
	journies_dict = result[1]
	# # continue
	# while found_shortest_path is False:
	# 	result = continue_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
	# 	found_shortest_path = result[0]
	# 	journies_dict = result[1]
	# modify the return object
	journey_path = None
	for journey_id in journies_dict:
		journey_path = journies_dict[journey_id]
	# return
	return journey_path
	





