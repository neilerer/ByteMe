# imports
import json
import pickle
import merge_sort



# def json_to_dict(file_name):
# 	with open(file_name) as json_data:
# 		return json.load(json_data)

# def key_to_list(key):
# 	key_list = key.split("-")
# 	return key_list



# def route(jpi_dict, jpi, weekday_input, hour_input):
# 	data = jpi_dict[jpi]
# 	#
# 	output_dict = dict()
# 	#
# 	for key in data:
# 		key_list = key_to_list(key)
# 		stop_sequence = key_list[0]
# 		stop_id = key_list[1]
# 		weekday = key_list[2]
# 		hour = key_list[3]
# 		ctt = data[key]

# 		if weekday == weekday_input and hour == hour_input:
# 			output_dict[stop_sequence] = (stop_id, ctt, jpi)
# 	#
# 	output_dict = merge_sort.merge_sort_route(output_dict)
# 	#
# 	return output_dict

# def route_list(output_dict):
# 	stop_id_list = []
# 	ctt_list = []
# 	jpi_list = []
# 	for stop_sequence in output_dict:
# 		value = output_dict[stop_sequence]
# 		stop_id = value[0]
# 		ctt = value[1]
# 		jpi = value[2]
# 		stop_id_list.append(stop_id)
# 		ctt_list.append(ctt)
# 		jpi_list.append(jpi)
# 	return [stop_id_list, ctt_list, jpi_list]

# def pathfinder_input(route_list_output):
# 	pathfinder_dict = dict()
# 	stop_id_list = route_list_output[0]
# 	ctt_list = route_list_output[1]
# 	jpi_list = route_list_output[2]
# 	index = 1
# 	for stop_id in stop_id_list[1::1]:
# 		start_stop_id = int(stop_id_list[index - 1])
# 		next_stop_id = int(stop_id_list[index])
# 		time = ctt_list[index] - ctt_list[index - 1]
# 		route = jpi_list[index - 1][0:5]
# 		quadruple = (start_stop_id, next_stop_id, time, route)
# 		pathfinder_dict[start_stop_id] = [quadruple]
# 		index += 1
# 	return pathfinder_dict



# def create_dict(start, end):
# 	this_dict = dict()
# 	for i in range(start, end, 1):
# 		this_dict[i] = dict()
# 	return this_dict

# def create_pathfinder_dictionary(outer_start, outer_end, inner_start, inner_end):
# 	pathfinder_dict = create_dict(outer_start, outer_end)
# 	for weekday in pathfinder_dict:
# 		pathfinder_dict[weekday] = create_dict(inner_start, inner_end)
# 	return pathfinder_dict

# def generate_pathfinder_input(file_name, outer_start, outer_end, inner_start, inner_end):
# 	pathfinder_dict = create_pathfinder_dictionary(outer_start, outer_end, inner_start, inner_end)
# 	jpi_dict = json_to_dict(file_name)
# 	for jpi in jpi_dict:
# 		for w in range(outer_start, outer_end, 1):
# 			weekday = str(w)
# 			for t in range(inner_start, inner_end, 1):
# 				time_unit = str(t)
# 				jpi_route_dict = route(jpi_dict, jpi, weekday, time_unit)
# 				jpi_route_lists = route_list(jpi_route_dict)
# 				jpi_pathfinder_input = pathfinder_input(jpi_route_lists)
# 				#
# 				destination_dict = pathfinder_dict[int(weekday)][int(time_unit)]
# 				for stop in jpi_pathfinder_input:
# 					stop_details = jpi_pathfinder_input[stop]
# 					for detail in stop_details:
# 						try:
# 							destination_dict[stop].append(detail)
# 						except:
# 							destination_dict[stop] = stop_details
# 	return pathfinder_dict



def json_to_dict(file_name):
	with open(file_name) as json_data:
		return json.load(json_data)



def key_to_list(key):
	key_list = key.split("-")
	return key_list



def unpack_observation(model_dict, jpi, key):
	# unpack the data
	key_data = key_to_list(key)
	stop_sequence = int(key_data[0])
	stop_id = int(key_data[1])
	weekday = int(key_data[2])
	time_unit = int(key_data[3])
	ctt = float(model_dict[jpi][key])
	route = jpi[0:5]
	# return
	return [weekday, time_unit, route, stop_sequence, stop_id, ctt]

def generate_jpi_dict_shell():
	# create the outermost layer
	shell_dict = dict()
	# iterate over the weekdays
	for i in range(0, 7, 1):
		shell_dict[i] = dict()
		# iterate over the hours in the day
		for j in range(0, 24, 1):
			shell_dict[i][j] = list()
	# return
	return shell_dict

def get_jpi_observations(model_dict, jpi):
	# create jpi_dict
	jpi_dict = generate_jpi_dict_shell()
	# iterate over the keys
	for key in model_dict[jpi]:
		# unpack
		observation = unpack_observation(model_dict, jpi, key)
		weekday = observation[0]
		time_unit = observation[1]
		# add to jpi_dict
		time_unit_dict = jpi_dict[weekday][time_unit]
		# add the observationt to the appropriate location
		jpi_dict[weekday][time_unit].append(observation)
	return jpi_dict

def get_key(a_list):
	return a_list[3]

def sort_jpi_observations(jpi_dict):
	for weekday in jpi_dict:
		for time_unit in jpi_dict[weekday]:
			time_unit_list = jpi_dict[weekday][time_unit]
			time_unit_list = sorted(time_unit_list, key=get_key)
			jpi_dict[weekday][time_unit] = time_unit_list
	return jpi_dict

def modify_jpi_time(jpi_dict):
	for weekday in jpi_dict:
		for time_unit in jpi_dict[weekday]:
			time_unit_list = jpi_dict[weekday][time_unit]
			prior_ctt = 0
			for observation in time_unit_list:
				ctt = observation[5]
				observation[5] = ctt - prior_ctt
				prior_ctt = ctt
	return jpi_dict

def jpi_into_pathfinder_format(jpi_dict):
	for weekday in jpi_dict:
		for time_unit in jpi_dict[weekday]:
			# data
			time_unit_list = jpi_dict[weekday][time_unit]
			new_time_unit_list = list()
			# iteration
			length = len(time_unit_list)
			index = 1
			while index < length:
				# data
				current = time_unit_list[index]
				prior = time_unit_list[index - 1]
				# quadruple = (start_stop_id, next_stop_id, time, route)
				quadruple = (prior[4], current[4], current[5], prior[2])
				new_time_unit_list.append(quadruple)
				index += 1
				# last entry check
				if index == length:
					new_time_unit_list.append((current[4], current[4], 0.00, prior[2]))
			# update the list
			jpi_dict[weekday][time_unit] = new_time_unit_list
	# return
	return jpi_dict

def jpi_unpacking(model_dict, jpi):
	jpi_dict = get_jpi_observations(model_dict, jpi)
	jpi_dict = sort_jpi_observations(jpi_dict)
	jpi_dict = modify_jpi_time(jpi_dict)
	jpi_dict = jpi_into_pathfinder_format(jpi_dict)
	return jpi_dict



def generate_pathfinder_dict_shell():
	# create the outermost layer
	shell_dict = dict()
	# iterate over the weekdays
	for i in range(0, 7, 1):
		shell_dict[i] = dict()
		# iterate over the hours in the day
		for j in range(0, 24, 1):
			shell_dict[i][j] = dict()
	# return
	return shell_dict

def create_pathfinder_dict(model_dict):
	# create the shell
	pathfinder_dict = generate_pathfinder_dict_shell()
	# populate the shell by iterating over the model_dict
	for jpi in model_dict:
		jpi_dict = jpi_unpacking(model_dict, jpi)
		for weekday in jpi_dict:
			for time_unit in jpi_dict[weekday]:
				# destination_dict
				destination_dict = pathfinder_dict[weekday][time_unit]
				# get all the stops from which you could start
				for quadruple in jpi_dict[weekday][time_unit]:
					stop = quadruple[0]
					if stop in destination_dict:
						destination_dict[stop].append(quadruple)
					else:
						destination_dict[stop] = [quadruple]
	# return
	return pathfinder_dict



# def create_jpi_dict(model_dict, jpi):
# 	# create jpi_dict
# 	# jpi_dict = generate_dict_shell()
# 	# iterate over the keys
# 	for key in model_dict[jpi]:
# 		# unpack
# 		observation = unpack_observation(model_dict, jpi, key)
# 		weekday = observation[0]
# 		time_unit = observation[1]
# 		route = observation[2]
# 		stop_sequence = observation[3]
# 		stop_id = observation[4]
# 		ctt = observation[5]
# 		# add to jpi_dict
# 		time_unit_dict = jpi_dict[weekday][time_unit]
# 		if stop_id in time_unit_dict:
# 			time_unit_dict[stop_id].append([route, stop_sequence, stop_id, ctt])
# 		else:
# 			time_unit_dict[stop_id] = [[route, stop_sequence, stop_id, ctt]]
# 	return jpi_dict












if __name__ == "__main__":
	# data
	model_dict = json_to_dict("data.json")
	# pathfinder_dict
	pathfinder_dict = create_pathfinder_dict(model_dict)
	destination = open("data2.p", "wb")
	# dump the data into the pickle file
	pickle.dump(pathfinder_dict, destination)
	# close the file
	destination.close()

	# # load the model data
	# model_dict = json_to_dict("data.json")
	# jpi_dict = get_jpi_observations(model_dict, "046A1001")
	# jpi_dict = sort_jpi_observations(jpi_dict)
	# jpi_dict = modify_jpi_time(jpi_dict)
	# jpi_dict = jpi_into_pathfinder_format(jpi_dict)
	# for weekday in jpi_dict:
	# 	for time_unit in jpi_dict[weekday]:
	# 		print(weekday, time_unit)
	# 		print(jpi_dict[weekday][time_unit])
	# 		print("")
	


	# for weekday in pathfinder_dict:
	# 	for time_unit in pathfinder_dict[weekday]:
	# 		print(weekday)
	# 		print(time_unit)
	# 		print(len(pathfinder_dict[weekday][time_unit]))
	# 		print("")
	# 	print("")
	# 	print("")


	# #
	# jpi = "046A1001"
	# for key in model_dict[jpi]:
	# 	print(unpack_observation(model_dict, jpi, key))

	# # first layer of dictionaries
	# print("Thees are the JPIs: ")
	# for jpi in model_dict:
	# 	print(jpi)
	# print("")
	# print("")
	# print("")

	# # examining the inner layers
	# print("This is 046A1001")
	# route_dict = model_dict["046A1001"]
	# for key in route_dict:
	# 	# unpack the data
	# 	key_data = key_to_list(key)
	# 	stop_sequence = key_data[0]
	# 	stop_id = key_data[1]
	# 	weekday = key_data[2]
	# 	time_unit = key_data[3]
	# 	ctt = route_dict[key]
	# 	# review
	# 	print(key)
	# 	print("Stop Sequence {}".format(stop_sequence))
	# 	print("Stop ID {}".format(stop_id))
	# 	print("Weekday {}".format(weekday))
	# 	print("Time Unit {}".format(time_unit))
	# 	print("CTT {}".format(ctt))
	# 	print("")
	# print("")
	# print("")
	# print("")






	# # # get shit to file
	# # pathfinder_dict = generate_pathfinder_input("data.json", 0, 7, 0, 24)
	# # destination = open("data.p", "wb")
	# # # dump the data into the pickle file
	# # pickle.dump(pathfinder_dict, destination)
	# # # close the file
	# # destination.close()