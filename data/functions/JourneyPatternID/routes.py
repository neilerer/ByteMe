# imports
import os
import glob


def weekday_data(file_name):
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