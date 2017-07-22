# imports
import os
import pickle

# DIRECTORY CHANGES
# dijkstra to pathfinder data
def d_to_pd():
	os.chdir("../../")
	os.chdir("data/data/pathfinder/")
def pd_to_d():
	os.chdir("../../../")
	os.chdir("pathfinder/dijkstra")


# SOURCE DATA
def next_stop_from_file():
	# got the appropriate directory
	d_to_pd()
	# open the pickle file
	f = open("next_stop.p", "rb")
	# load the pickle file
	next_stop_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# return to the appropriate dictory
	pd_to_d()
	# return
	return next_stop_dict