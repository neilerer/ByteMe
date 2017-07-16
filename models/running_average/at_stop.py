# imports
import os
import glob
import general


def stop_coordinates_all(file_name):
	# data
	headers = general.headers_list(file_name)
	bus_stops_by_day = general.bus_stops_all(file_name)
	source = general.open_bus_stop_all_read(file_name)
	# skip the first line
	source.readline()
	# coordinates
	coordinates = []
	for line in source:
		line_list = line.strip().split(",")
		lat = line_list[headers.index("Latitude")]
		lon = line_list[headers.index("Longitude")]
		coordinates.append((lat, lon))
	source.close()
	return coordinates



# 	0	1	  2		3	4		5		6		7		8		9		10			11				12			13				14		15			16		17		  18		19		20		30		31		32				33			34				35			 	36				37			38					39				40			 41		42	
# Year,Month,Day,Hours,Minute,Second,WeekDay,YearDay,Timestamp,LineID,Direction,JourneyPatternID,TimeFrame,VehicleJourneyID,Operator,Congestion,Longitude,Latitude,BusDelay,BlockID,VehicleID,StopID,AtStop,Temperature (C),Dew Point (C),Humidity (%),Pressure (hPa),Visibility (km),Wind Direction,Wind Speed (km/h),Gust Speed (km/h),Precipitation,Events,Conditions