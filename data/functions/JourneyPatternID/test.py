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


jpi_preview("00010001.csv")