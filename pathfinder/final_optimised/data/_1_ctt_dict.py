# imports
import glob
import json
import os
import pickle



def json_to_dict(file_name):
	with open(file_name) as json_data:
		return json.load(json_data)



def unpack_observation(json_data, jpi, key):
	key_list = key.strip().split("-")
	# return (weekday, time_unit, route, stop_sequence, stop_id, ctt)
	return (int(key_list[2]), int(key_list[3]), jpi[0:5], int(key_list[0]), int(key_list[1]), float(json_data[jpi][key]))



def create_ctt_dict(json_data):
	ctt_dict = dict()
	for i in range(0, 7, 1):
		ctt_dict[i] = dict()
		for j in range(0, 24, 1):
			ctt_dict[i][j] = dict()
	return ctt_dict

def generate_ctt_dict(json_data):
	# create_ctt_dict
	ctt_dict = create_ctt_dict(json_data)
	# iterate over the individual files
	for file_name in glob.glob("ctt_dict_*"):
		# get the data
		f = open(file_name, "rb")
		route_dict = pickle.load(f)
		f.close()
		# add it to ctt_dict
		for weekday in route_dict:
			for time_unit in route_dict[weekday]:
				for route in route_dict[weekday][time_unit]:
					ctt_dict[weekday][time_unit][route] = route_dict[weekday][time_unit][route]
	# save ctt_dict
	destination = open("ctt_dict.p", "wb")
	pickle.dump(ctt_dict, destination)
	destination.close()

def clean_up():
	for file_name in glob.glob("ctt_dict_*"):
		os.remove(file_name)

if __name__ == "__main__":
	json_data = json_to_dict("data.json")
	generate_ctt_dict(json_data)
	clean_up()