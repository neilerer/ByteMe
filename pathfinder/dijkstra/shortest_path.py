# imports
import general
import data_conversion


"""
been_list
journies_dict
- {journey_id : [time, journey]}
-- journey_id is str
-- time is float
-- journy is list of stop details
--- stop details (start stop, next stop, next time, route)
"""



def check_if_already_been(stop_id, been_list):
	return (stopid in been_list)

def possible_next_stops(list_of_stop_details, been_list):
	next_stop_list = []
	for stop_detail in list_of_stop_details:
		next_stop = stop_detail[1]
		if not check_if_already_been(next_stop, been_list):
			next_stop_list.append(next_stop)
	return next_stop_list



def continue_journey(journey_id, stop_id, stop_dict, journies_list, been_list):
	list_of_stop_details = stop_dict[stop_id]
	for stop_detail in list_of_stop_details:
		next_stop = stop_detail[1]
		next_time = stop_detail[2]
		next_route = stop_detail[3]
		if next_stop in been_list:
			pass
		else:
