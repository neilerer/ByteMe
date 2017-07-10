# imports
import os
import glob
import headers
import stops_raw


"""
This file was used to a few tests and quick views while developing.
"""


# utility functions
def jpif_to_jpid():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")

def jpid_to_jpif():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")


def jpi_preview(file_name):
	# change directory
	jpif_to_jpid()
	# open file
	with open(file_name, "r") as source:
		# reference objects
		header = source.readline().strip().split(",")
		data = source.readline().strip().split(",")
		# display the data
		counter = 0
		counter_bound = len(header)
		while counter < counter_bound:
			print(header[counter] + ": " + data[counter])
			counter += 1
	# change directory
	jpid_to_jpif()



# my_list = ["040D0001.csv",
# "00410001.csv",
# "01451005.csv",
# "066B0001.csv",
# "01110001.csv",
# "033X0001.csv",
# "032B0002.csv",
# "00830006.csv",
# "00071001.csv",
# "00171003.csv",
# "00160003.csv"]
# for data in my_list:
# 	data = stops_raw.weekday_data(data)
# 	print(data[1])

data = stops_raw.weekday_data("00010001.csv")
print(data[0])