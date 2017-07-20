# imports
import os
import glob


# DIRECTORY CHANGES
# data_collection to bus_stop data
def dc_to_bsd():
	os.chdir("../../../")
	os.chdir("data/data/JourneyPatternID/bus_stops")
def bsd_to_dc():
	os.chdir("../../../../")
	os.chdir("pathfinder/data_collection/bus_stops")


# FILE NAMES
# list of bus files
def list_of_bus_files():
	# change directory
	dc_to_bsd()
	# collect all the file names
	csv_list = []
	for file in glob.glob("*.csv"):
		csv_list.append(file)
	# change directory
	bsd_to_dc()
	# return
	return csv_list


# READ FILES
# bus stop data
def read_bus_stop_data(file_name):
	"""
	Remember to close the file when you're done with it
	"""
	# change directory
	dc_to_bsd()
	# open the file
	source = open(file_name, "r")
	# return to starting direcotyr
	bsd_to_dc()
	# return the open file
	return source


# RETURN DATA
# bus stop data
def return_bus_stop_data(file_name):
	source = read_bus_stop_data(file_name)
	bus_stops = source.readline().strip().split(",")
	source.close()
	return bus_stops