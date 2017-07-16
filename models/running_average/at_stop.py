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


def bus_stop_all_coordinates_at_stop(file_name):
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
		if at_stop == '1':
			if sid in temp_dict:
				temp_dict[sid].append((lat, lon, at_stop))
			else:
				temp_dict[sid] = [(lat, lon, at_stop)]
	source.close()
	return coordinates


def bus_stop_all_average_coordinates(coordinates_by_weekday, weekday, stop_id):
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
	# calculat return values
	lat_all = 0
	lon_all = 0
	lat_at_stop = 0
	lon_at_stop = 0
	# all
	try:
		lat_all = lat_total_all / count_all
		lon_all = lon_total_all / count_all
	except:
		lat_all = None
		lon_all = None
	# at stop
	try:
		lat_at_stop = lat_total_at_stop / count_at_stop
		lon_at_stop = lon_total_at_stop / count_at_stop
	except:
		lat_at_stop = None
		lat_at_stop = None
	# return
	return [(lat_all, lon_all), (lat_at_stop, lon_at_stop)]


file_name = "00010001.csv"
coordinates_by_weekday = bus_stop_all_coordinates_at_stop(file_name)
for triple in bus_stop_all_average_coordinates(coordinates_by_weekday, 0, '226'):
	print(triple)


# def bus_stop_range_coordinates_min_max(lat_min, lon_min, lat_max, lon_max, lat, lon):
# 	# lat
# 	if lat < lat_min:
# 		lat_min = lat
# 	elif lat > lat_max:
# 		lat_max = lat
# 	else:
# 		pass
# 	# lon
# 	if lon < lon_min:
# 		lon_min = lon
# 	elif lon > lon_max:
# 		lon_max = lon
# 	else:
# 		pass
# 	return [lat_min, lon_min, lat_max, lon_max]

# def bus_stop_range(coordinates_by_weekday, weekday, sid):
# 	# primary data object
# 	coordinates = coordinates_by_weekday[weekday][sid]
# 	# starting figures
# 	lat_min = float(coordinates[0])
# 	lat_max = float(lat_min)
# 	lon_min = float(coordinates[1])
# 	lon_max = float(lon_min)
# 	# iteratively find the min and max
# 	for pair in coordinates[1::1]:
# 		lat = float(pair[0])
# 		lon = float(pair[1])
# 		new_vals = bus_stop_range_coordinates_min_max(lat_min, lon_min, lat_max, lon_max, lat, lon)
# 		lat_min, lon_min, lat_max, lon_max = new_vals[0], new_vals[1], new_vals[2], new_vals[3]
# 	# return
# 	return [(lat_min, lon_max), (lat_max, lon_min)]


# 	0	1	  2		3	4		5		6		7		8		9		10			11				12			13				14		15			16		17		  18		19		20		30		31		32				33			34				35			 	36				37			38					39				40			 41		42	
# Year,Month,Day,Hours,Minute,Second,WeekDay,YearDay,Timestamp,LineID,Direction,JourneyPatternID,TimeFrame,VehicleJourneyID,Operator,Congestion,Longitude,Latitude,BusDelay,BlockID,VehicleID,StopID,AtStop,Temperature (C),Dew Point (C),Humidity (%),Pressure (hPa),Visibility (km),Wind Direction,Wind Speed (km/h),Gust Speed (km/h),Precipitation,Events,Conditions