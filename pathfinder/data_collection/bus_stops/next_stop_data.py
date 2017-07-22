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


def next_stop_from_file():
	# got the appropriate directory
	general.dc_to_pd()
	# open the pickle file
	f = open("next_stop.p", "rb")
	# load the pickle file
	next_stop_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# return to the appropriate dictory
	general.pd_to_dc()
	# return
	return jpi_intersections


if __name__ == "__main__":
	status = (next_stop.next_for_all() == next_stop_from_file())
	print("A new dictionary and that form file match: {}".format(status))