# imports
import pickle
import general
import next_stop


def next_stop_to_file():
	# generate the data
	next_stop_dict = next_stop.next_for_all()
	# got to the directory
	general.dc_to_pd()
	# create the pickle file
	destination = open("next_stop.p", "wb")
	# dump the data into the pickle file
	pickle.dump(next_stop_dict, destination)
	# close the file
	destination.close()
	# return to the starting directory
	general.pd_to_dc()


next_stop_to_file()