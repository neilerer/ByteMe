# imports
import data_conversion_model_to_path as dcmtp



def get_path_data():
	return dcmtp.model_data_to_path_data()



def get_bus_stop_data():
	path_data = get_path_data()
	stop_dict = dict()
	for path_id in path_data:
		path = path_data[path_id]
		for stop in path:
			stop_details = path[stop]
			stop_id = stop_details[0]
			next_stop_id = stop_details[1]
			journey_time = stop_details[2]
			if stop in stop_dict:
				stop_dict[stop].append((stop_id, next_stop_id, journey_time, path_id))
			else:
				stop_dict[stop] = [(stop_id, next_stop_id, journey_time, path_id)]
	# sort based on travel time
	for stop in stop_dict:
		stop_list = stop_dict[stop]
		stop_list.sort(key=lambda tup: tup[2])
	return stop_dict

bus_stop_data = get_bus_stop_data()
for stop in bus_stop_data:
	print(stop)
	print(bus_stop_data[stop])
	print("")

"""
Get unique bus stops
Create dicitonary with bus stop id as key
- value is list
-- list contains every triple of (stop_id, next_stop_id, journey_time)
"""