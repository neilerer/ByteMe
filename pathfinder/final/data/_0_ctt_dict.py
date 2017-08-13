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

def generate_ctt_dict(file_name):
	# shell
	ctt_dict = dict()
	for i in range(0, 7, 1):
		ctt_dict[i] = dict()
		for j in range(0, 24, 1):
			ctt_dict[i][j] = dict()
	# source data
	json_data = json_to_dict(file_name)
	# populate ctt_dict
	for jpi in json_data:
		for key in json_data[jpi]:
			for key in json_data[jpi]:
				data = unpack_observation(json_data, jpi, key)
				destination = ctt_dict[data[0]][data[1]]
				if data[2] in destination:
					destination[data[2]].append((data[3], data[4], data[5]))
				else:
					destination[data[2]] = [(data[3], data[4], data[5])]
	# sort the route-level data
	for weekday in ctt_dict:
		for time_unit in ctt_dict[weekday]:
			for route in ctt_dict[weekday][time_unit]:
				ctt_dict[weekday][time_unit][route] = sorted(ctt_dict[weekday][time_unit][route], key = itemgetter(0))
	# return
	return ctt_dict



if __name__ == "__main__":
	# data
	ctt_dict = generate_ctt_dict("data.json")
	destination = open("ctt_dict.p", "wb")
	# dump the data into the pickle file
	pickle.dump(ctt_dict, destination)
	# close the file
	destination.close()