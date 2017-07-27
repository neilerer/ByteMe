# imports
import general



def get_model_data():
	return general.test_data_from_file()



def dict_to_list(route):
	stop_list = []
	ctt_list = []
	for stop in route:
		ctt = route[stop]
		stop_list.append(stop)
		ctt_list.append(ctt)
	return [stop_list, ctt_list]

def get_route_journey_time_dict(dict_to_list_output):
	stop_list = dict_to_list_output[0]
	ctt_list = dict_to_list_output[1]
	route_journey_time_dict = dict()
	end_index = len(stop_list) - 1
	for stop in stop_list:
		stop_index = stop_list.index(stop)
		stop_ctt = ctt_list[stop_index]
		if stop_index != end_index:
			next_stop = stop_list[stop_index + 1]
			next_ctt = ctt_list[stop_index + 1]
			journey_time = next_ctt - stop_ctt
			data = (stop, next_stop, journey_time)
			route_journey_time_dict[stop] = data
	return route_journey_time_dict

def model_data_to_path_data():
	path_data_dict = dict()
	model_data = get_model_data()
	for route_id in model_data:
		route = model_data[route_id]
		dict_to_list_output = dict_to_list(route)
		path_data_dict[route_id] = get_route_journey_time_dict(dict_to_list_output)
	return path_data_dict



if __name__ == "__main__":
	path_data = model_data_to_path_data()
	for item in path_data:
		print(item)
		print(path_data[item])
		print("")