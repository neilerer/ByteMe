# imports
import json
from operator import itemgetter
import pickle



def json_to_dict(file_name):
	with open(file_name) as json_data:
		return json.load(json_data)



def unpack_observation(json_data, jpi, key):
	key_list = key.strip().split("-")
	# return (weekday, time_unit, route, stop_sequence, stop_id, ctt)
	return (int(key_list[2]), int(key_list[3]), jpi[0:5], int(key_list[0]), int(key_list[1]), float(json_data[jpi][key]))



def generate_ctt_dict(json_data):
	# high level structure
	ctt_dict = dict()
	for i in range(0, 7, 1):
		ctt_dict[i] = dict()
		for j in range(0, 24, 1):
			ctt_dict[i][j] = dict()
	# detailed structure
	for jpi in json_data:
		for key in json_data[jpi]:
			data = unpack_observation(json_data, jpi, key)
			destination = ctt_dict[data[0]][data[1]]
			if data[2] in destination:
				pass
			else:
				destination[data[2]] = list()
	return ctt_dict

def populate_ctt_dict_for_given_jpi(json_data, ctt_dict, jpi):
	# populate ctt_dict
	for key in json_data[jpi]:
		for key in json_data[jpi]:
			data = unpack_observation(json_data, jpi, key)
			destination = ctt_dict[data[0]][data[1]]
			destination[data[2]].append((data[3], data[4], data[5]))

def sort_ctt_dict(ctt_dict):
	# sort the route-level data
	for weekday in ctt_dict:
		for time_unit in ctt_dict[weekday]:
			for route in ctt_dict[weekday][time_unit]:
				ctt_dict[weekday][time_unit][route] = sorted(ctt_dict[weekday][time_unit][route], key = itemgetter(0))
	# return
	return ctt_dict



if __name__ == "__main__":
	# data
	json_data = json_to_dict("data.json")
	# generate ctt_dict
	ctt_dict = generate_ctt_dict(json_data)
	ctt_dict = populate_ctt_dict_for_given_jpi(json_data, ctt_dict, "077A1001")
	ctt_dict = sort_ctt_dict(ctt_dict)
	# get it to file
	destination = open("ctt_dict.p", "wb")
	# dump the data into the pickle file
	pickle.dump(ctt_dict, destination)
	# close the file
	destination.close()