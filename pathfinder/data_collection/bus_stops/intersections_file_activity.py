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


def intersections_from_file():
	# got the appropriate directory
	general.dc_to_i()
	# open the pickle file
	f = open("jpi_intersections.p", "rb")
	# load the pickle file
	jpi_intersections = pickle.load(f)
	# close the pickle file
	f.close()
	# return to the appropriate dictory
	general.i_to_dc()
	# return
	return jpi_intersections


# if __name__ == "__main__":
# # 	intersections_to_file()
# 	test = intersections_from_file()
# 	actual = intersections.get_all_intersections()
# 	if test == actual:
# 		print("OK")
# 	else:
# 		print("Not OK")