# imports
import copy
import merge_sort



def time_unit_model_dict(weekday, time_unit, model_dict):
	# time_unit_dict
	return model_dict[weekday][time_unit]

def start_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict):
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	if start_stop_id == end_stop_id:
		return [True, {0 :[0.00, [(start_stop_id, end_stop_id, 0.00, None) ] ] } ]
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
	# instantiate starting_dict
	continuing_dict = journies_dict
	# sort starting_dict so that the shortest journey is considered
	continuing_dict = merge_sort.merge_sort_journies_dict(starting_dict)
	# continue the shortest journey
	current_journey = merge_sort.remove_first_entry_of_dict(continuing_dict)
	# unpack current_journey
	journey_id = current_journey[0]
	current_journey_contents = current_journey[1]
	current_journey_time = current_journey_contents[0]
	been_set = current_journey_contents[1]
	current_stop_id = current_journey_contents[2][-1][1]
	# determine if this journey will be continued
	# iterate over the quadruples of the next stop; extend the journey if a quadruple hasn't been visited before