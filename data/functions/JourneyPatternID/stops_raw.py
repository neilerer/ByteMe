# imports
import os
import stops_raw

"""
These functions are used to extract raw information from the JourneyPatternID files that are then refined by other functions
"""


"""
This functions searches the relevant file and identifies all the unique weekday values
"""
def weekday_values(file_name):
	# weekdays
	weekdays = set()
	# find source file
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# open source file
	with open(file_name, "r") as source:
		# find the index by using the first line
		index = source.readline().strip().split(",").index("WeekDay")
		# iterate over the data lines
		for line in source:
			# convert line to list
			line_list = source.readline().strip().split(",")
			# try add WeekDay values to the set
			try:
				weekdays.add(line_list[index])
			# if no value, skip
			except:
				pass
	# convert set to an array
	weekdays = list(weekdays)
	# sort the list
	weekdays.sort()
	# go back to starting directory
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID/")
	# return
	return weekdays


"""
This function returns two items:
- weekday_lists: a list for each weekday that contains tuples of (Timestamp, StopID)
- weekdays: list of weekday values from the file

Use if you want raw data by weekday for a given JPI
"""
def weekday_data(file_name):
	# create the files
	weekdays = weekday_values(file_name)
	# change directories
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# open the source
	with open(file_name, "r") as source:
		# index the columns of interest using the header line
		header_list = source.readline().strip().split(",")
		index_wd = header_list.index("WeekDay")
		index_ts = header_list.index("Timestamp")
		index_sid = header_list.index("StopID")
		index_as = header_list.index("AtStop")
		index_vjid = header_list.index("VehicleJourneyID")
		index_vid = header_list.index("VehicleID")
		# weekday lists
		weekday_lists = [[] for item in weekdays]
		# iterate over the data lines
		for line in source:
			# turn line into list
			line_list = line.strip().split(",")
			try:
				# if it's at a stop
				if line_list[index_as] == '1':
					# generate an integer value of the WeekDay value for indexing
					wd = int(line_list[index_wd])
					# add, to the appropriate weekday list, a tuple of (Timestamp, StopID)
					weekday_lists[wd].append((line_list[index_ts], line_list[index_sid], line_list[index_vjid] + "_" + line_list[index_vid]))
			except:
				# if the line_list doesn't have an AtStop value, then it's blank
				pass
	# change directory
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")
	# modify weekdays
	weekdays = [int(x) for x in weekdays]
	# return
	return [weekday_lists, weekdays]


#NEEDS TO BE CHANGED TO ACCOMODATE THE VJID_VID COLUMN
"""
This creates files to store weekday_data, if desired
"""
def weekday_files(file_name):
	# weekdays
	weekdays = weekday_values(file_name)
	# change directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/stops")
	# iterate over the files
	for wd in weekdays:
		# new_name
		new_name = file_name.strip().split(".")[0] + "_" + wd + ".csv"
		# create the file
		with open(new_name, "w") as source:
			# add the headers
			source.write("Timestamp,StopID" + "\n")
	# change directory
	os.chdir("../../../")
	os.chdir("functions/JourneyPatternID/")


"""
This generates and writes the weekday_data information to file
"""
def weekday_data_to_file(file_name):
	# create the files
	weekday_files(file_name)
	# create the data
	wd_data = weekday_data(file_name)
	data = wd_data[0]
	weekdays = wd_data[1]
	# weekdays_file_names
	weekdays_file_names = [file_name.strip().split(".")[0] + "_" + wd + ".csv" for wd in weekdays]
	# change directories
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/stops/")
	# modify weekdays
	weekdays = [int(x) for x in weekdays]
	# populate the files
	for day in weekdays:
		# open the destination file
		with open(weekdays_file_names[day], "a") as destination:
			# iterate over the data tuples
			for pair in data[day]:
				# write to the file
				destination.write(",".join(pair) + "\n")


"""
Below here is where I futz about with the code while in development
"""
# file_name = "00010001reduced.csv"