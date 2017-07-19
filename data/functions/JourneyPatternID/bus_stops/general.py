# imports
import os
import glob


# DIRECTORY CHANGES
#
def bsf_to_jpi():
	os.chdir("../../../")
	os.chdir("data/JourneyPatternID/")
def jpi_to_bsf():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID/bus_stops")
#
def bsf_to_bsd():
	os.chdir("../../../")
	os.chdir("data/JourneyPatternID/bus_stops")
def bsd_to_bsf():
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID/bus_stops")


# OPEN FILE
def read_jpi_file(file_name):
	"""
	Remember to close the file when you're done with it
	"""
	# change directory
	bsf_to_jpi()
	# open the file
	source = open(file_name, "r")
	# return to starting direcotyr
	jpi_to_bsf()
	# return the open file
	return source


# HEADERS
def headers_list(file_name):
	source = read_jpi_file(file_name)
	headers = source.readline().strip().split(",")
	source.close()
	return headers


def list_of_csv_files():
	# change directory
	bsf_to_jpi()
	# collect all the file names
	csv_list = []
	for file in glob.glob("*.csv"):
		csv_list.append(file)
	# change directory
	jpi_to_bsf()
	# return
	return csv_list