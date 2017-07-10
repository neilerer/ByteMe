# imports
import os
import glob
import routes_comp_functions as rcf

"""
These functions get us the stops on a jpi for each day of the week
"""

"""
Used to remove key:value pairs in which the value list has only one element (not useful in imputing route)
"""
def remove_single_values(wd_dict):
	kill_list = []
	for key in wd_dict:
		if len(wd_dict[key]) == 1:
			kill_list.append(key)
	for item in kill_list:
		del wd_dict[item]

"""
Extracts each journeys on a jpi, grouped by weekday 
"""
def weekday_stops(file_name):
	# change directories
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# open the source
	with open(file_name, "r") as source:
		# header
		header = source.readline().strip().split(",")
		# index
		index_wd = header.index("WeekDay")
		index_vjid = header.index("VehicleJourneyID")
		index_vid = header.index("VehicleID")
		index_sid = header.index("StopID")
		# weekday lists
		weekday_dicts = [{} for i in range(0, 7, 1)]
		# iterate over the source document
		for line in source:
			# turn line into list
			line_list = line.strip().split(",")
			try:
				# values
				wd = int(line_list[index_wd])
				vjid = line_list[index_vjid]
				vid = line_list[index_vid]
				uid = vjid + "_" + vid
				# data objects
				uid_dict = weekday_dicts[wd]
				stop_id = line_list[index_sid]
				# if the uid is in the dictionary
				if uid in uid_dict:
					# specify the list that is the value to the uid's key
					stop_list = uid_dict[uid]
					# if the stop_id is different from the last element in the stop_list
					if stop_list[-1] != stop_id:
						# add it to the array
						stop_list.append(stop_id)
				else:
					# create the dictionary
					uid_dict[uid] = [stop_id]
			except:
				pass
		# return to the starting directory
		os.chdir("../../")
		os.chdir("functions/JourneyPatternID")
		# remove elements with just one entry
		for i in range(0, 7, 1):
			wd_dict = weekday_dicts[i]
			remove_single_values(wd_dict)
		# return
		return weekday_dicts


"""
Quick testing section
"""
file = "00010001.csv"
data = weekday_stops(file)
print("")
print("File:", file)
print("")
for i in range(0, 7, 1):
	print("Weekday:", i)
	result = rcf.route_for_jpi_on_weekday(data, i)
	print("Route:", result)
	print("")