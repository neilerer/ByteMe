# imports
import os
import bus_stops_general as general


def remove_single_values(wd_dict):
	"""
	Purpose
	- used to remove key:value pairs in which the value list has only one element (not useful in imputing route)
	- used withing journeys()
	Inputs
	- wd_dict: dictionary for a given weekday containing key:value of VJID_VID:[StopID list]
	- generated within journeys()
	Outputs
	- None
	- this function modifes the dictionary in place
	"""
	kill_list = []
	# iterate over dictionary keys
	for key in wd_dict:
		# if the associated list has only one element
		if len(wd_dict[key]) == 1:
			# mark this dictionary entry for deletion
			kill_list.append(key)
	# iterate over the keys in kill_list
	for item in kill_list:
		# delete that entry from the dictionary
		del wd_dict[item]

def routes(file_name):
	# data
	headers = general.headers_list(file_name)
	source = general.read_jpi_file(file_name)
	# index values
	index_wd = headers.index("WeekDay")
	index_yd = headers.index("YearDay")
	index_vjid = headers.index("VehicleJourneyID")
	index_vid = headers.index("VehicleID")
	index_sid = headers.index("StopID")
	# return object
	unique_journeys = {}
	# skip the first line
	source.readline()
	# iterate over each line
	for line in source:
		# turn line into a list
		line_list = line.strip().split(",")
		try:
			# create data
			wd = line_list[index_wd]
			yd = line_list[index_yd]
			vjid = line_list[index_vjid]
			vid = line_list[index_vid]
			sid = line_list[index_sid]
			# modify data
			uid = "{}_{}_{}_{}".format(vjid, vid, wd, yd)
			# check if the uid has already been recorded
			if uid in unique_journeys:
				# check if it was the most recently recorded
				if unique_journeys[uid][-1] == sid:
					# skip it if it was; we only want stops, not idles
					pass
				else:
					# add it to the list otherwise
					unique_journeys[uid].append(sid)
			else:
				# create the dictionary entry
				unique_journeys[uid] = [sid]
		except:
			# if the line does not have the data, skip it
			pass
	# remove single entries
	remove_single_values(unique_journeys)
	# return
	return unique_journeys

# my_dict = routes("00010001.csv")
# for item in my_dict:
# 	print(my_dict[item])