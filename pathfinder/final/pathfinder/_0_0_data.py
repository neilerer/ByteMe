# imports
import json
import os
import pickle



def get_pickle_file(file_name):
	# change directory
	os.chdir("../")
	os.chdir("data")
	# pickle activities
	f = open(file_name, "rb")
	python_data = pickle.load(f)
	f.close()
	# change directory
	# change directory
	os.chdir("../")
	os.chdir("pathfinder")
	return python_data





def get_model_data():
	# change directory
	os.chdir("../")
	os.chdir("data")
	# get shit from file
	f = open("data.p", "rb")
	# load the pickle file
	model_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("pathfinder")
	# return
	return model_dict


def get_actual_model_data():
	# change directory
	os.chdir("../")
	os.chdir("data")
	# get shit from file
	f = open("data.json")
	json_data = json.load(f)
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("pathfinder")
	# return
	return json_data


if __name__ == "__main__":
	json_data = get_actual_model_data()
	for jpi in json_data:
		for key in json_data[jpi]:
			print(item)


