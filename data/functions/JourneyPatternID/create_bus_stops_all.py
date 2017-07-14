# imports
import os
import glob
import bus_stops


def list_of_csv_files():
	# change directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/")
	# collect all the file names
	csv_list = []
	for file in glob.glob("*.csv"):
		csv_list.append(file)
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")
	# return
	return csv_list


def create_file(file_name):
	# collect the data
	data = bus_stops.bus_stops_for_jpi_all(file_name)
	# change directory
	os.chdir("../../")
	os.chdir("data/JourneyPatternID/bus_stops/all")
	# make the file
	with open(file_name, "w") as destination:
		for day in data:
			destination.write(",".join(day) + "\n")
	# change directory
	os.chdir("../../../../")
	os.chdir("functions/JourneyPatternID")

 
def create_files():
	files = list_of_csv_files()
	for file_name in files:
		create_file(file_name)


if __name__ == "__main__":
	create_files()