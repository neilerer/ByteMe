# imports
import copy



def time_unit_model_dict(weekday, time_unit, model_dict):
	# time_unit_dict
	return model_dict[weekday][time_unit]

def start_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, been_list, journey_id_list):
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	if start_stop_id == end_stop_id:
		return [True, {0 : (start_stop_id, end_stop_id, 0.00, None)}]
	# ending_dict
	ending_dict = dict()
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
		journey_id = 0
	# record that we've been to this bus stop
	been_list.append(start_stop_id)
	# find the quadruples associated with potential next stops
	list_of_start_stop_quadruples = time_unit_dict[start_stop_id]
	# populate ending_dict
	for stop_id in list_of_start_stop_quadruples:
		# extract information
		start_quadruple = list_of_start_stop_quadruples[stop_id]
		next_stop_id = start_quadruple[1]
		next_stop_journey_time = start_quadruple[2]
		next_stop_route = start_quadruple[3]
		if (next_stop_id not in been_list) and (next_stop_route in path):
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			ending_dict[journey_id] = [start_quadruple]
			# increment the journey_id
			journey_id += 1
	# return
	return [False, ending_dict]