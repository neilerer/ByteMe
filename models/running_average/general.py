# imports
import os
import glob


# DIRECTORY CHANGES
# bus_stop
def ra_to_bus_stops_all():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID/bus_stops/all")

def bus_stops_all_to_ra():
	os.chdir("../../../../../")
	os.chdir("models/running_average")

# JourneyPaternID
def ra_to_jpid():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID")

def jpid_to_ra():
	os.chdir("../../../")
	os.chdir("models/running_average")


# files names
def get_jpi_file_names():
	file_names = []
	ra_to_jpid()
	for file in glob.glob("*.csv"):
		file_names.append(file)
	jpid_to_ra()
	return file_names


# reading files
def open_jpi_source_read(file_name):
	"""
	Remember to close the file when you're done with it
	"""
	# change directory
	ra_to_jpid()
	# open the file
	source = open(file_name, "r")
	# return to starting direcotyr
	jpid_to_ra()
	# return the open file
	return source

def headers_list(file_name):
	source = open_jpi_source_read(file_name)
	headers = source.readline().strip().split(",")
	source.close()
	return headers

def headers_string(file_name):
	source = open_jpi_source_read(file_name)
	headers = source.readline().strip()
	source.close()
	return headers

ra_to_bus_stops_all()
bus_stops_all_to_ra()