# imports
import os
import glob


def jpi_to_bus_all():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/bus_stops/all")

def lines_in_file(file_name):
	count = 0
	with open(file_name, "r") as source:
		for line in source:
			count += 1
	return count

jpi_to_bus_all()
print(lines_in_file("00010001.csv"))