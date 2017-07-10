# imports
import os
import glob
import headers


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



jpi_preview("00411003.csv")

# jpif_to_jpid()
# with open("00010001reduced.csv", "r") as file:
# 	for i in range(0, 100, 1):
# 		print(file.readline().strip())

source = "00411003.csv"
test_array = [['5044', '45', '3694', '3696', '49', '50', '277', '288'], ['4432', '119', [['4432', '119', '45', '47', '48', '49', '277', '288'], ['5044', '3696', '49', '52', '277', '288'], ['5044', '3694', '3698', '45', '47', '49', '277', '288'], ['5044', '5079', '3694', '3696', '1637', '1638', '1639', '1640', '213', '44', '45', '47', '277', '288'], ['5044', '4432', '44', '45', '46', '48', '49', '51', '52', '277'], ['5044', '46', '49', '50', '277', '288'], ['5044', '213', '48', '49', '52', '277', '288'], ['5044', '3694', '3696', '231', '1642', '213', '46', '49', '277', '288'], [...]], '45', '47', '48', '49', '51', '52', '277', '288'], ['5044', '3694', '3696', '3698', '1637', '1639', '1641', '214', '45', '46', '47', '48', '49', '277'], ['5044', '5079', '3694', '3695', '3696', '1636', '1637', '1638', '1639', '1640', '231', '119', '44', '45', '48', '49', '50', '52', '277'], ['5044', '3697'], 'NoRoute', 'NoRoute']

for item in test_array:
	print(item)