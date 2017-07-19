# imports
import os
import glob


# making sure each file has seven lines
def jpi_to_bus_all():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/bus_stops/all")

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
	bus_all_to_jpi()
	return [lines, lines == expected_lines]

def get_bus_stop_file_names():
	file_names = []
	jpi_to_bus_all()
	for file in glob.glob("*.csv"):
		file_names.append(file)
	bus_all_to_jpi()
	return file_names

def check_lines():
	with open("quality_bus_stops_all_seven_lines.txt", "w") as destination:
		file_names = get_bus_stop_file_names()
		for file_name in file_names:
			result = check_lines_in_file(file_name, 7)
			if not result[1]:
				destination.write("{}: {}".format(file_name, result[0]) + "\n")

if __name__ == "__main__":
	check_lines()