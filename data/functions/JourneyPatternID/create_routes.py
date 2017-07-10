# imports
import os
import glob
import create_stop_files as csf


"""
This function creates the files to save each record of the bus being at a stop for a given jpi and weekday combination
"""
def create_directories():
	# source of names
	source_of_names = csf.files_to_use()
	# change directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/routes")
	# create the files: one for each jpi and weekday combination
	for file in source_of_names:
		# name of the directory
		name = file.strip().split(".")[0]
		# check if the directory alredy exists
		if os.path.exists(name + "/"):
			# directory already exists
			pass
		else:
			# make a directory for the jpi
			os.mkdir(name)
			# change directory
			os.chdir(name + "/")
			# make a directory for each weekday
			for i in range(0, 7, 1):
				os.mkdir(str(i))
			# change directory
			os.chdir("../")
	# change directory
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID")


def create_route(source_file, destination_file, headers):
	# get input for stop_keep_index
	stopid_index = headers.index("StopID")
	# go to soure file
	#
	# open source file: 
	with open(source_file, "r") as source:
		# go to destination file
		# 
		# open destination file
		with open(destination_file, "w") as destination:
			current = source.readline().strip().split("")
			destination.write(",".join(current) + "\n")
			prior = current
			prior_stop_id = prior[stopid_index]
			for line in source:
				current = source.readline().strip().split(",")
				current_stop_id = current[stopid_index]
				if current_stop_id == prior_stop_id:
					pass
				else:
					destination.write(",".join(current) + "\n")
					prior = current
					prior_stop_id = prior[stopid_index]


def create_routes():
	# 
	source_of_names = csf.files_to_use()
	# 
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/stop_and_idle")
	# 
	
	




def make_routes():
	create_directories()
