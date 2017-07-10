# imports
import os
import glob


"""
This function generates an array of each jpi file to use
"""
def files_to_use():
	# file_name_holder
	file_name_holder = []
	# go to directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")
	# iterate over the source files
	for file in glob.glob("*.csv"):
		# add the file name
		file_name_holder.append(file)
	# return to the starting directory
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")
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
	os.chdir("data/JourneyPatternID/stop_and_idle")
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


"""
This function populates the appropriate files: a sequential order of stops taken by a bus on a jpi on a weekday
"""
def populate_files():
	# change directory
	os.chdir("../../")
	os.chdir("data/combined/")
	# open source
	with open("combined.csv", "r") as source:
		# change directory
		os.chdir("../")
		os.chdir("JourneyPatternID/stop_and_idle/")
		# define headers
		headers = source.readline().strip().split(",")
		# index list
		weekday_index = headers.index("WeekDay")
		jpi_index = headers.index("JourneyPatternID")
		atstop_index = headers.index("AtStop")
		stopid_index = headers.index("StopID")
		vjid_index = headers.index("VehicleJourneyID")
		vid_index = headers.index("VehicleID")
		timestamp_index = headers.index("Timestamp")
		length = len(headers)
		length_range = range(0, length, 1)
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
				# if the bus is at a stop
				if at_stop == "1":
					# change directory
					os.chdir(jpi + "/" + weekday + "/")
					# determine file name
					name = vjid + "_" + vid
					file_name = name + ".csv"
					# if the file exists
					if os.path.exists(file_name):
						# create and populate a storage list for existing information
						storage_list = []
						with open(file_name, "r") as temp_source:
							for i in length_range:
								storage_list.append(readline())
						# add the new information to the stored informaiton
						for i in length_range:
							storage_list[i] = storage_list[i] + line_list[i] + ","
						# write the information back to file
						with open(file_name, "w") as destination:
							for item in storage_list:
								destination.write(item + "\n")
					else:
						# otherwise create the file and add the data
						with open(file_name, "w") as destination:
							for item in line_list:
								destination.write(item + ",")
					# change directory
					os.chdir("../../")
			except:
				# no data in the line
				pass
	# return to the starting directory
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID/")


"""
This function creates the README.txt file
"""
def read_me():
	# change directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/stop_and_idle")
	# create the file
	with open("README.txt", "w") as destination:
		# intro lines
		first_line = "Each line contains all the recorded AtStop==1 information for a UID = VJID_VID\n"
		second_line = "The rows represent:\n"
		destination.write(first_line)
		destination.write(second_line)
		# data lines
		os.chdir("../../")
		os.chdir("combined")
		# get headers
		headers = []
		with open("combined.csv", "r") as source:
			headers = source.readline().strip().split(",")
		for h in headers:
			destination.write(h + "\n")
	# return to starting directory
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")


"""
This function aggregates all the elements of this file
"""
def all_recorded_stops():
	read_me()
	create_directories()
	populate_files()


if __name__ == "__main__":
	all_recorded_stops()