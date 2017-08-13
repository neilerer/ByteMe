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


if __name__ == "__main__":
	json_data = get_actual_model_data()
	for jpi in json_data:
		for key in json_data[jpi]:
			print(item)


