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



model_data = get_model_data()
route = model_data[1]
for item in dict_to_list(route):
	print(item)
print(get_route_journey_time_dict(dict_to_list(route)))