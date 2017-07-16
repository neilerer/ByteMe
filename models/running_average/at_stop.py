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
		# add the information to coordinates
		weekday = int(line_list[headers.index("WeekDay")])
		temp_dict = coordinates[weekday]
		if sid in temp_dict:
			temp_dict[sid].append((lat, lon))
		else:
			temp_dict[sid] = [(lat, lon)]
	source.close()
	return coordinates

coordinates = bus_stop_all_coordinates("00010001.csv")
monday = coordinates[0]
monday_226 = monday['226']
# starting figures
lat_min = float(monday_226[0][0])
lat_max = float(lat_min)
lon_min = float(monday_226[0][1])
lon_max = float(lon_min)
for pair in monday_226[1::1]:
	lat = float(pair[0])
	lon = float(pair[1])
	if lat < lat_min:
		lat_min = lat
	elif lat > lat_max:
		lat_max = lat
	else:
		pass
	if lon < lon_min:
		lon_min = lon
	elif lon > lon_max:
		lon_max = lon
	else:
		pass
print("Lat range is {} to {}".format(lat_min, lat_max))
print("Lon range in {} to {}".format(lon_min, lon_max))


# 	0	1	  2		3	4		5		6		7		8		9		10			11				12			13				14		15			16		17		  18		19		20		30		31		32				33			34				35			 	36				37			38					39				40			 41		42	
# Year,Month,Day,Hours,Minute,Second,WeekDay,YearDay,Timestamp,LineID,Direction,JourneyPatternID,TimeFrame,VehicleJourneyID,Operator,Congestion,Longitude,Latitude,BusDelay,BlockID,VehicleID,StopID,AtStop,Temperature (C),Dew Point (C),Humidity (%),Pressure (hPa),Visibility (km),Wind Direction,Wind Speed (km/h),Gust Speed (km/h),Precipitation,Events,Conditions