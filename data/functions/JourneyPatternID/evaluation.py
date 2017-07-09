# imports
import os
import glob
import headers


# utility functions
def jpif_to_jpid():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")

def jpid_to_jpif():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")


# unique values
def unique_values(source, header_list):
	# index_list
	index_list = [headers.headers_reduced.index(header) for header in header_list]
	# unique_values
	unique_values_list = [set() for i in index_list]
	# skip the first line
	source.readline()
	# populate the set
	for line in source:
		line_list = line.strip().split(",")
		counter = 0
		counter_bound = len(index_list)
		while counter < counter_bound:
			unique_values_list[counter].add(line_list[index_list[counter]])
			counter += 1
	# return
	return [sorted(list(x)) for x in unique_values_list]


def get_unique_values(file_name, header_list):
	# change directory
	jpif_to_jpid()
	# open the file
	with open(file_name, "r") as source:
		# return to the starting directory
		jpid_to_jpif()
		# return
		return unique_values(source, header_list)


# jpif_to_jpid()
# for item in get_unique_values("00010001reduced.csv", ["VehicleJourneyID", "VehicleID"]):
# 	print(item)