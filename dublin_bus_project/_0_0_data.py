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