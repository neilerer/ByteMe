# imports
import os
import pickle



# GET DATA
def get_rc_connections_dict():
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
	os.chdir("possible_paths_review")
	# return
	return connections_dict



def connections_dict_review():
	connections_dict = get_rc_connections_dict()
	with open("connections_dict_review.txt", "w") as destination:
		for weekday in connections_dict:
			destination.write("Weekday: {}\n\n\n".format(weekday))
			weekday_data = connections_dict[weekday]
			for time_unit in weekday_data:
				destination.write("Time Unit: {}\n".format(time_unit))
				time_unit_data = weekday_data[time_unit]
				for route in time_unit_data:
					destination.write("{}: ".format(route))
					route_data = time_unit_data[route]
					for connected_route in route_data:
						destination.write("{}, ".format(connected_route))
					destination.write("\n")
			destination.write("\n\n")
		destination.write("\n\n\n\n")



if __name__ == "__main__":
	connections_dict_review()