# imports
import os
import pickle



def get_model_data():
	# change directory
	# get shit from file
	f = open("data.p", "rb")
	# load the pickle file
	model_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	# return
	return model_dict