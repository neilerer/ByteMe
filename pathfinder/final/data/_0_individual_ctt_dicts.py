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

def generate_data_to_populate_ctt_dict(json_data, weekday, time_unit, jpi):
	# output_list
	output_list = list()
	# populate ctt_dict
	for key in json_data[jpi]:
		data = unpack_observation(json_data, jpi, key)
		if data[0] == weekday and data[1] == time_unit:
			output_list.append((data[3], data[4], data[5]))
	# sort the output_list
	output_list = sorted(output_list, key=itemgetter(0))
	# return output_list
	return output_list



if __name__ == "__main__":
	# data
	json_data = json_to_dict("data.json")

	# populate ctt_dict
	for jpi in json_data:
		# high level structure
		ctt_dict = dict()
		for i in range(0, 7, 1):
			ctt_dict[i] = dict()
			for j in range(0, 24, 1):
				ctt_dict[i][j] = dict()
		# route
		route = jpi[0:5]
		for weekday in ctt_dict:
			for time_unit in ctt_dict[weekday]:
				ctt_dict[weekday][time_unit][route] = generate_data_to_populate_ctt_dict(json_data, weekday, time_unit, jpi)
				destination = open("ctt_dict_" + route + ".p", "wb")
				pickle.dump(ctt_dict, destination)
				destination.close()