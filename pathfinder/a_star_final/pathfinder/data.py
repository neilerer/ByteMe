# imports
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