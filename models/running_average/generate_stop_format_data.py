# imports
import change_directories
import get_file_names
import source_data



def get_jpi_names():
	change_directories.to_jpi()
	jpi_names = get_file_names.all_csv()
	change_directories.from_jpi()
	return jpi_names



def get_headers():
	# data objects
	headers_list = list()
	jpi_names = get_jpi_names()
	change_directories.to_jpi()
	for jpi in jpi_names:
		jpi_data = source_data.open_jpi(jpi)
		header = jpi_data.readline().strip().split(",")
		headers_list.append(header)
		jpi_data.close()
	change_directories.from_jpi()
	# confirm each header is identical
	prime = headers_list[0]
	for header in headers_list[1:0:1]:
		if prime != header:
			return None
	return prime



def 


# ['Year', 'Month', 'Day', 'Hours', 'Minute', 'Second', 'WeekDay', 'YearDay', 'Timestamp', 'LineID', 'Direction', 'JourneyPatternID', 'TimeFrame', 'VehicleJourneyID', 'Operator', 'Congestion', 'Longitude', 'Latitude', 'BusDelay', 'BlockID', 'VehicleID', 'StopID', 'AtStop', 'Temperature (C)', 'Dew Point (C)', 'Humidity (%)', 'Pressure (hPa)', 'Visibility (km)', 'Wind Direction', 'Wind Speed (km/h)', 'Gust Speed (km/h)', 'Precipitation', 'Events', 'Conditions']
# ['WeekDay', 'Hours', 'Minute', 'Second', 'Timestamp', 'StopID', 'JourneyPatternID', 'VehicleJourneyID', 'VehicleID', 'Longitude', 'Latitude', 'Conditions']