# imports
import os
import glob
import stops_raw
import stops_refined


"""
These functions will use the end-function of stops_refined to generate bus route and save them to file
"""

"""
This function generates an array of each jpi file to use
"""
def files_to_use():
	# file_name_holder
	file_name_holder = []
	# go to directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# iterate over the source files
	for file in glob.glob("*.csv"):
		# add the file name
		file_name_holder.append(file)
	# return to the starting directory
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID/")
	# return
	return file_name_holder


"""
This function generates the route data to write to file
"""
def route_data_to_write(file):
	# array to hold routes for each day of the week
	route_holder = []
	# iterate over the weekdays
	for i in range(0, 7, 1):
		try:
			# record the route
			data = stops_refined.route_for_jpi_on_weekday(file, i)
			route_holder.append(data)
		except:
			# or record that no route exists
			route_holder.append("NoRoute")
	# reutrn the route holder
	return route_holder


"""
This function writes the generated data to file
"""
def write_route_to_file(file):
	# data
	route_holder = route_data_to_write(file)
	print(route_holder) # delete me
	# change directories
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/stops/")
	# record the data
	with open(file, "w") as destination:
		for route in route_holder: # initial problem
			destination.write(",".join(route) + "\n")
	# return to the starting directory
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID/")


"""
This file aggregates the prior functions
"""
def record_stops():
	# generate the array of JourneyPatternIDs
	jpi_array = files_to_use()
	# iterate over them
	for jpi in jpi_array:
		write_route_to_file(jpi)


# if __name__ == "__main__":
# 	record_stops()

write_route_to_file("00010001.csv")