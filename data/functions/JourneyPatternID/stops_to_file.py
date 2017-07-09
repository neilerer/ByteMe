# imports
import os
import glob
import stops_raw
import stops_refined


"""
These functions will use the end-function of stops_refined to generate bus route and save them to file
"""


def record_stops():
	# go to directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# iterate over the source files
	for file in glob.glob("*.csv"):
		# create data holder
		data_holder = []
		# change directory to collect data
		os.chdir("../../")
		os.chdir("functions/JourneyPatternID/")
		# collect the data
		for i in range(0, 7, 1):
			try:
				data_holder.append(stops_refined.route_for_jpi_on_weekday(file, i))
			except:
				data_holder.append(None)
		# change directory to the source file
		os.chdir("../../")
		os.chdir("data/JourneyPatternID/")
		# open the source file
		with open(file, "r") as source:
			# go to the approprite directory
			os.chdir("stops/")
			# open the destination file
			with open(file, "w") as destination:
				# iterate over the routes
				for route in data_holder:
					# write to the destination
					destination.write(",".join(route) + "\n")
	# return to the starting directory
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID/")


if __name__ == "__main__":
	record_stops()