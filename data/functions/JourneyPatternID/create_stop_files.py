# imports
import os
import glob
import headers


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
This function creates the files to save each record of the bus being at a stop for a given jpi and weekday combination
"""
def create_directories():
	# source of names
	source_of_names = files_to_use()
	# change directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/stops")
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
	os.chdir("functions/JourneyPatternID/")


"""
This function populates the appropriate files: a sequential order of stops taken by a bus on a jpi on a weekday
"""
def populate_files():
	# index list
	headers_reduced = headers.headers
	weekday_index = headers_reduced.index("WeekDay")
	jpi_index = headers_reduced.index("JourneyPatternID")
	atstop_index = headers_reduced.index("AtStop")
	stopid_index = headers_reduced.index("StopID")
	vjid_index = headers_reduced.index("VehicleJourneyID")
	vid_index = headers_reduced.index("VehicleID")
	# change directory
	os.chdir("../../")
	os.chdir("data/combined/")
	# open source
	with open("combined.csv", "r") as source:
		# change directory
		os.chdir("../")
		os.chdir("JourneyPatternID/stops/")
		# skip the first line
		source.readline()
		# iterate over data in the combined file
		for line in source:
			line_list = line.strip().split(",")
			try:
				# variables
				at_stop = line_list[atstop_index]
				jpi = line_list[jpi_index]
				weekday = line_list[weekday_index]
				vjid = line_list[vjid_index]
				vid = line_list[vid_index]
				stop_id = line_list[stopid_index]
				# if the bus is at a stop
				if at_stop == "1":
					print("found a stop") # DELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETE
					# change directory
					os.chdir(jpi + "/" + weekday + "/")
					# determine file name
					name = vjid + "_" + vid
					file_name = name + ".csv"
					# if the file exists
					if os.path.exists(file_name):
						# append the StopID
						print("wrote something") # DELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETE
						with open(file_name, "a") as destination:
							destination.write(stop_id + ",")
					else:
						print("wrote something") # DELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETEDELETE
						# otherwise create the file and add the StopID
						with open(file_name, "w") as destination:
							destination.write(stop_id + ",")
					# change directory
					os.chdir("../../")
			except:
				# no data in the line
				pass
	# return to the starting directory
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID/")


"""
This function aggregates all the elements of this file
"""
def all_recorded_stops():
	create_directories()
	populate_files()


if __name__ == "__main__":
	all_recorded_stops()