# imports
import pickle
import general
import intersections


def intersections_to_file():
	# generate the dictionary
	jpi_intersections = intersections.get_all_intersections()
	# got the appropriate directory
	general.dc_to_i()
	# create the file
	destination = open("jpi_intersections.p", "wb")
	# get the dictionary to disk
	pickle.dump(jpi_intersections, destination)
	# close the file
	destination.close()
	# return to the starting directory
	general.i_to_dc()


if __name__ == "__main__":
	intersections_to_file()