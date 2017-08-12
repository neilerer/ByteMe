# imports
import json
import os
import pickle



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