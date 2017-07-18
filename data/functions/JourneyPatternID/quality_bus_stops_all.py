# imports
import os
import glob


def jpi_to_bus_all():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")
	# os.chdir("data/JourneyPatternID/bus_stops/all")

def bus_all_to_jpi():
	os.chdir("../../../../")
	os.chdir("functions/JourneyPatternID")

def lines_in_file(file_name):
	count = 0
	with open(file_name, "r") as source:
		for line in source:
			count += 1
	return count

def check_lines_in_file(file_name, expected_lines):
	jpi_to_bus_all()
	lines = lines_in_file(file_name)
	jpi_to_bus_all()
	return lines == expected_lines

print(check_lines_in_file("00010001.csv", 7))