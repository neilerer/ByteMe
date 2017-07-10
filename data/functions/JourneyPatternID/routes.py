# imports
import os
import glob
<<<<<<< HEAD


def weekday_data(file_name):
=======
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
>>>>>>> data
	# change directories
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# open the source
	with open(file_name, "r") as source:
<<<<<<< HEAD
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
=======
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
>>>>>>> data
		for line in source:
			# turn line into list
			line_list = line.strip().split(",")
			try:
<<<<<<< HEAD
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
=======
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
testing
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


# file_name = "00010001.csv"

# data = weekday_stops(file_name)

# result = rcf.route_for_jpi_on_weekday(data, 0)
# print(result)
# print(len(result))


# # for item in data[0]:
# # 	print(data[0][item])
# uid_list = ["5461_38002", "5494_33492", "5512_33459", "5444_38001", "5425_33494"]
# primary_array = data[0][uid_list[0]]
# secondary_array = data[0][uid_list[2]]
# not_in = rcf.not_in_primary_details(primary_array, secondary_array)
# print(primary_array)
# print(secondary_array)
# print(not_in)
>>>>>>> data
