# imports
import os
import glob


"""
These functions are used to extract and save information from the combined csv file and regroup it by JourneyPatternID
"""


# directory functions
def jpif_to_combined():
	os.chdir("../../")
	os.chdir("data/combined")

def combined_to_jpifd():
	os.chdir("../JourneyPatternID")

def jpif_to_jpid():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")

def jpid_to_jpif():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")


def unique_journey_pattern_ids(file_name):
	uji_set = set()
	jpif_to_combined()
	with open(file_name, "r") as source:
		headers = source.readline().strip().split(",")
		offset = headers.index("JourneyPatternID")
		for line in source:
			line_list = line.strip().split(",")
			if len(line_list) == 0 or len(line_list) == 1:
				pass
			else:
				

#def create_destination_files(file_name):



def get_raw_data(file_name):
	# change directories
	jpif_to_combined()
	# open source
	with open(file_name, "r") as source:
		# change directory
		combined_to_jpifd()
		# record the headers
		headers = source.readline()
		# 