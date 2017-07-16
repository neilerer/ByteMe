# imports
import os
import glob


# DIRECTORY CHANGES
# bus_stop_all
def ra_to_bus_stops_all():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID/bus_stops/all")

def bus_stops_all_to_ra():
	os.chdir("../../../../../")
	os.chdir("models/running_average")

# bus_stop_weekdays_constant
def ra_to_bus_stops_weekdays_constant():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID/bus_stops/weekdays_constant")

def bus_stops_weekdays_constant_to_ra():
	os.chdir("../../../../../")
	os.chdir("models/running_average")

# JourneyPaternID
def ra_to_jpid():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID")

def jpid_to_ra():
	os.chdir("../../../")
	os.chdir("models/running_average")


# FILES NAMES
# bus_stops_all
def get_bus_stop_all_file_names():
	file_names = []
	ra_to_bus_stops_all()
	for file in glob.glob("*.csv"):
		file_names.append(file)
	bus_stops_all_to_ra()
	return file_names

# bus_stops_weekdays_constant
def get_bus_stop_weekdays_constant_file_names():
	file_names = []
	ra_to_bus_stops_weekdays_constant()
	for file in glob.glob("*.csv"):
		file_names.append(file)
	bus_stops_weekdays_constant_to_ra()
	return file_names

# jpi_file_names
def get_jpi_file_names():
	file_names = []
	ra_to_jpid()
	for file in glob.glob("*.csv"):
		file_names.append(file)
	jpid_to_ra()
	return file_names


# READING FILES
# bus_stops_all
def open_bus_stop_all_read(file_name):
	"""
	Remember to close the file when you're done with it
	"""
	# change directory
	ra_to_bus_stops_all()
	# open the file
	source = open(file_name, "r")
	# return to starting direcotyr
	bus_stops_all_to_ra()
	# return the open file
	return source

# bus_stops_weekdays_constant
def open_bus_stop_weekdays_constant_read(file_name):
	"""
	Remember to close the file when you're done with it
	"""
	# change directory
	ra_to_bus_stops_weekdays_constant()
	# open the file
	source = open(file_name, "r")
	# return to starting direcotyr
	bus_stops_weekdays_constant_to_ra()
	# return the open file
	return source

# jpi
def open_jpi_source_read(file_name):
	"""
	Remember to close the file when you're done with it
	"""
	# change directory
	ra_to_jpid()
	# open the file
	source = open(file_name, "r")
	# return to starting direcotyr
	jpid_to_ra()
	# return the open file
	return source


# HEADERS
# list
def headers_list(file_name):
	source = open_jpi_source_read(file_name)
	headers = source.readline().strip().split(",")
	source.close()
	return headers

# string
def headers_string(file_name):
	source = open_jpi_source_read(file_name)
	headers = source.readline().strip()
	source.close()
	return headers


# BUS STOPS
def bus_stops_all(file_name):
	source = open_bus_stop_all_read(file_name)
	bus_stops_by_day = []
	for line in source:
		bus_stops_by_day.append(tuple(line.strip().split(",")))
	source.close()
	return bus_stops_by_day

print(bus_stops_all("00010001.csv"))


# 	0	1	  2		3	4		5		6		7		8		9		10			11				12			13				14		15			16		17		  18		19		20		30		31		32				33			34				35			 	36				37			38					39				40			 41		42	
# Year,Month,Day,Hours,Minute,Second,WeekDay,YearDay,Timestamp,LineID,Direction,JourneyPatternID,TimeFrame,VehicleJourneyID,Operator,Congestion,Longitude,Latitude,BusDelay,BlockID,VehicleID,StopID,AtStop,Temperature (C),Dew Point (C),Humidity (%),Pressure (hPa),Visibility (km),Wind Direction,Wind Speed (km/h),Gust Speed (km/h),Precipitation,Events,Conditions


