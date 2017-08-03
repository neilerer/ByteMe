# imports
import json
import pickle
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



def create_dict(start, end):
	this_dict = dict()
	for i in range(start, end, 1):
		this_dict[i] = dict()
	return this_dict

def create_pathfinder_dictionary(outer_start, outer_end, inner_start, inner_end):
	pathfinder_dict = create_dict(outer_start, outer_end)
	for weekday in pathfinder_dict:
		pathfinder_dict[weekday] = create_dict(inner_start, inner_end)
	return pathfinder_dict

def generate_pathfinder_input(file_name, outer_start, outer_end, inner_start, inner_end):
	pathfinder_dict = create_pathfinder_dictionary(outer_start, outer_end, inner_start, inner_end)
	jpi_dict = json_to_dict(file_name)
	for jpi in jpi_dict:
		for w in range(outer_start, outer_end, 1):
			weekday = str(w)
			for t in range(inner_start, inner_end, 1):
				time_unit = str(t)
				jpi_route_dict = route(jpi_dict, jpi, weekday, time_unit)
				jpi_route_lists = route_list(jpi_route_dict)
				jpi_pathfinder_input = pathfinder_input(jpi_route_lists)
				#
				destination_dict = pathfinder_dict[int(weekday)][int(time_unit)]
				for stop in jpi_pathfinder_input:
					stop_details = jpi_pathfinder_input[stop]
					for detail in stop_details:
						try:
							destination_dict[stop].append(detail)
						except:
							destination_dict[stop] = stop_details
	return pathfinder_dict




if __name__ == "__main__":
	# # get shit to file
	# pathfinder_dict = generate_pathfinder_input("data_for_pathfinder.json", 0, 7, 0, 23)
	# destination = open("pathfinder_data.p", "wb")
	# # dump the data into the pickle file
	# pickle.dump(pathfinder_dict, destination)
	# # close the file
	# destination.close()


	# get shit from file
	f = open("pathfinder_data.p", "rb")
	# load the pickle file
	pathfinder_dict = pickle.load(f)
	# close the pickle file
	f.close()


	monday = pathfinder_dict[0]
	nine_oclock = monday[9]
	for stop in nine_oclock:
		print(stop)
		print(nine_oclock[stop])
		print("")

	# for weekday in pathfinder_dict:
	# 	day_dict = pathfinder_dict[weekday]
	# 	for time_unit in day_dict:
	# 		time_unit_dict = day_dict[time_unit]
	# 		for stop in time_unit_dict:
	# 			stop_list = time_unit_dict[stop]
	# 			print(weekday)
	# 			print(time_unit)
	# 			print(stop)
	# 			print(stop_list)
	# 			print("")


	# dict_display("data_for_pathfinder.json", "046A0001")

	
	# jpi_dict = json_to_dict("data_for_pathfinder.json")
	# jpi = "046A0001"
	# weekday_input = "1"
	# hour_input = "9"
	# my_route = route(jpi_dict, jpi, weekday_input, hour_input)
	# my_route_list = route_list(my_route)
	# print(pathfinder_input(my_route_list))