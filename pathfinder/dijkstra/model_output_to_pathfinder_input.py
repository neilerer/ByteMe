# imports
import json
import merge_sort



def json_to_dict(file_name):
	with open(file_name) as json_data:
		return json.load(json_data)

def key_to_list(key):
	key_list = key.split("-")
	return key_list

def dict_display(file_name, jpi):
	data = json_to_dict(file_name)[jpi]
	for key in data:
		key_list = key_to_list(key)
		print("Key: {}".format(key_list))
		print("Stop Sequence: {}".format(key_list[0]))
		print("Stop ID: {}".format(key_list[1]))
		print("Weekday: {}".format(key_list[2]))
		print("Hour: {}".format(key_list[3]))
		print("CTT: {}".format(data[key]))
		print("")

def route(jpi_dict, jpi, weekday_input, hour_input):
	data = jpi_dict[jpi]

	output_dict = dict()

	for key in data:
		key_list = key_to_list(key)
		stop_sequence = key_list[0]
		stop_id = key_list[1]
		weekday = key_list[2]
		hour = key_list[3]
		ctt = data[key]

		if weekday == weekday_input and hour == hour_input:
			output_dict[stop_sequence] = (stop_id, ctt, jpi)

	output_dict = merge_sort.merge_sort_route(output_dict)

	return output_dict

def route_list(output_dict):
	stop_id_list = []
	ctt_list = []
	jpi_list = []
	for stop_sequence in output_dict:
		value = output_dict[stop_sequence]
		stop_id = value[0]
		ctt = value[1]
		jpi = value[2]
		stop_id_list.append(stop_id)
		ctt_list.append(ctt)
		jpi_list.append(jpi)
	return [stop_id_list, ctt_list, jpi_list]

def pathfinder_input(route_list_output):
	pathfinder_dict = dict()
	stop_id_list = route_list_output[0]
	ctt_list = route_list_output[1]
	jpi_list = route_list_output[2]
	index = 1
	for stop_id in stop_id_list[1::1]:
		start_stop_id = int(stop_id_list[index - 1])
		next_stop_id = int(stop_id_list[index])
		time = ctt_list[index] - ctt_list[index - 1]
		route = jpi_list[index - 1][0:5]
		quadruple = (start_stop_id, next_stop_id, time, route)
		pathfinder_dict[start_stop_id] = [quadruple]
		index += 1
	return pathfinder_dict



jpi_dict = json_to_dict("data_for_pathfinder.json")
for jpi in jpi_dict:
	jpi_route_dict = route(jpi_dict, jpi, '3', '9')
	jpi_route_lists = route_list(jpi_route_dict)
	jpi_pathfinder_input = pathfinder_input(jpi_route_lists)
	print(jpi)
	for stop in jpi_pathfinder_input:
		print("")
		print(stop)
		print(jpi_pathfinder_input[stop])
	print("")
	print("")


# jpi_dict = json_to_dict("046A0001.json")
# my_dict = route(jpi_dict, "046A0001", '3', '9')
# my_lists = route_list(my_dict)
# for_pathfinder = pathfinder_input(my_lists)
# for stop in for_pathfinder:
# 	print(stop)
# 	print(for_pathfinder[stop])
# 	print("")