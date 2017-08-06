# imports
import os
import pickle


def get_model_data():
	# change directory
	os.chdir("../")
	os.chdir("data_json")
	# get shit from file
	f = open("data.p", "rb")
	# load the pickle file
	model_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("shortest_path")
	# return
	return model_dict


def get_connections_dict():
	# change directory
	os.chdir("../")
	os.chdir("possible_paths")
	# get shit from file
	f = open("rc_connections_dict.p", "rb")
	# load the pickle file
	connections_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("shortest_path")
	# return
	return connections_dict