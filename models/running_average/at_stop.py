# imports
import os
import glob
import general


def bus_stop_all_coordinates(file_name):
	# data
	headers = general.headers_list(file_name)
	source = general.open_jpi_source_read(file_name)
	# coordinates
	coordinates = [{} for day in range(0, 7, 1)]
	# skip the first line of the source
	source.readline()
	for line in source:
		# create the information to add to coordinates
		line_list = line.strip().split(",")
		sid = line_list[headers.index("StopID")]
		lat = line_list[headers.index("Latitude")]
		lon = line_list[headers.index("Longitude")]
		at_stop = line_list[headers.index("AtStop")]
		# add the information to coordinates
		weekday = int(line_list[headers.index("WeekDay")])
		temp_dict = coordinates[weekday]
		if sid in temp_dict:
			temp_dict[sid].append((lat, lon, at_stop))
		else:
			temp_dict[sid] = [(lat, lon, at_stop)]
	source.close()
	return coordinates


def coordinates_average(lat_total, lon_total, count):
	try:
		lat = lat_total / count
		lon = lon_total / count
	except:
		lat = None
		lon = None
	finally:
		return (lat, lon)

def bus_stop_average_coordinates(coordinates_by_weekday, weekday, stop_id):
	# primary data object
	coordinates = coordinates_by_weekday[weekday][stop_id]
	# values
	lat_total_all = 0
	lon_total_all = 0
	count_all = 0
	lat_total_at_stop = 0
	lon_total_at_stop = 0
	count_at_stop = 0
	# iteratively determine the average StopID coordinates
	for triple in coordinates:
		lat = float(triple[0])
		lon = float(triple[1])
		at_stop = int(triple[2])
		# all
		lat_total_all += lat
		lon_total_all += lon
		count_all += 1
		# at stop
		if at_stop == 1:
			lat_total_at_stop += lat
			lon_total_at_stop += lon
			count_at_stop += 1
	# all
	all_data = coordinates_average(lat_total_all, lon_total_all, count_all)
	# at stop
	at_stop_data = coordinates_average(lat_total_at_stop, lon_total_at_stop, count_at_stop)
	# return
	return [all_data, at_stop_data]


file_name = "00010001.csv"
coordinates_by_weekday = bus_stop_all_coordinates(file_name)
for i in range(0, 7, 1):
	coordinates = bus_stop_average_coordinates(coordinates_by_weekday, i, '226')
	print("")
	print("Bus Stop Coordintes for {} for All".format(i))
	print(coordinates[0])
	print("")
	print("Bus Stop Coordintes for {} for AtStop == 1".format(i))
	print(coordinates[1])




# 	0	1	  2		3	4		5		6		7		8		9		10			11				12			13				14		15			16		17		  18		19		20		30		31		32				33			34				35			 	36				37			38					39				40			 41		42	
# Year,Month,Day,Hours,Minute,Second,WeekDay,YearDay,Timestamp,LineID,Direction,JourneyPatternID,TimeFrame,VehicleJourneyID,Operator,Congestion,Longitude,Latitude,BusDelay,BlockID,VehicleID,StopID,AtStop,Temperature (C),Dew Point (C),Humidity (%),Pressure (hPa),Visibility (km),Wind Direction,Wind Speed (km/h),Gust Speed (km/h),Precipitation,Events,Conditions