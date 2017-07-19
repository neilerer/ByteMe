# imports
import os
import glob
import general


def stops_greater_than_one(file_name):
	# open the file
	source = general.read_bus_stop_file(file_name)
	# generate a list of the first line
	bus_stops = source.readline().strip().split(",")
	# return
	return len(bus_stops) > 1

def check_if_all_routes_are_greater_than_one():
	# file names
	file_names = general.list_of_csv_files()
	# hold object
	bad_files = []
	# iterate over file names
	for file_name in file_names:
		if not stops_greater_than_one(file_name):
			bad_files.append(file_name)
	# save results to file (if needed)
	if len(bad_files) > 0:
		with open("erroneous_bus_stops.txt", "w") as source:
			for item in bad_files:
				source.write(item + "\n")


def all_checks():
	check_if_all_routes_are_greater_than_one()

if __name__ == "__main__":
	all_checks()