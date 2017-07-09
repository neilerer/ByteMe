#imports
import os
import glob
import wd_headers

"""
This file contains some general functions used in various files in the weather section
"""


# General
def csv_line_to_list(line):
	# convert line to a list
	list_from_line = line.strip().split(',')
	# return object
	return list_from_line


# Time (GMT): Hour, Minute
def am_pm_to_24(am_pm):
	# variables
	time = am_pm.split()
	hour = time[0].split(":")[0]
	minute = time[0].split(":")[1]
	indicator = time[1]
	# covert hour
	if indicator == "PM":
		if hour != "12":
			hour = str(int(hour) + 12)
	else:
		if hour == "12":
			hour = str(0)
	return [hour, minute]

def wd_hour(time):
	return am_pm_to_24(time)[0]

def wd_minute(time):
	return am_pm_to_24(time)[1]


# Temp., Windchill, Dew Point: Temperature, Windchill, Dew Point
def wd_temp(temp):
	return temp.split()[0]


# Humidity: Humidity
def wd_humidity(humidity):
	return humidity.split("%")[0]


# 'Pressure': Pressure
def wd_pressure(pressure):
	return pressure.split()[0]


# 'Visibility': Visibility
def wd_visibility(visibility):
	return visibility.split()[0]


# Wind Dir: Wind Direction
def wd_wind_direction(wind_direction):
	return wind_direction


# Wind Speed
def wd_wind_speed(wind_speed):
	return wind_speed.split()[0]


# Gust Speed
def wd_gust_speed(gust_speed):
	return gust_speed.split()[0]


# Precipitation
def wd_precipitation(precipitation):
	return precipitation


# Events
def wd_events(events):
	return events


# Condtions
def wd_condition(conditions):
	return conditions