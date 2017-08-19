# imports
import json
import pickle
from operator import itemgetter



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
					new_time_unit_list.append((current[4], None, 0.00, prior[2]))
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
	# sort the stop level lists of quadruples by time so that when sourced in Dijkstra, they will be in appropriate order; we don't want to waste time sorting on every use of Dijkstra
	for weekday in pathfinder_dict:
		for time_unit in pathfinder_dict[weekday]:
			for stop in pathfinder_dict[weekday][time_unit]:
				list_of_quadruples = pathfinder_dict[weekday][time_unit][stop]
				pathfinder_dict[weekday][time_unit][stop] = sorted(list_of_quadruples,key=itemgetter(2))
	# return
	return pathfinder_dict



if __name__ == "__main__":
	# data
	model_dict = json_to_dict("data.json")
	# pathfinder_dict
	pathfinder_dict = create_pathfinder_dict(model_dict)
	destination = open("stop_dict.p", "wb")
	# dump the data into the pickle file
	pickle.dump(pathfinder_dict, destination)
	# close the file
	destination.close()