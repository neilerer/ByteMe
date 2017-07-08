# imports
import os
import glob

# global variables
headers_bus = ['Year', 'Month', 'Day', 'Hours', 'Minute', 'Second', 'WeekDay', 'YearDay', 'Timestamp', 'LineID', 'Direction', 'JourneyPatternID', 'TimeFrame', 'VehicleJourneyID', 'Operator', 'Congestion', 'Longitude', 'Latitude', 'BusDelay', 'BlockID', 'VehicleID', 'StopID', 'AtStop']

headers_weather = [
"Year", 
"Month", 
"Day", 
"Hours", 
"Minute", 
"Second", 
"Day of the Week (Monday == 0)", 
"Day of the Year (0 to 366)",
"Temperature (C)", # celcius
"Dew Point (C)", # celcius
"Humidity (%)", # %
"Pressure (hPa)", # hPa
"Visibility (km)", # km
"Wind Direction",
"Wind Speed (km/h)", # km/h
"Gust Speed (km/h)", # km/h
"Precipitation", 
"Events",
"Conditions",
]


def weather_count(counter, file_reference, prior_list, current_list):
	prior_list = current_list
	current_list = file_reference.readline().strip().split(",")
	counter += 1
	return [counter, prior_list, current_list]

def check_match_hour(ref_list, target_list):
	for i in range(0, 4, 1):
		if not ref_list[i] == target_list[i]:
			return False
	return True

def check_over_minute(ref_list, target_list):
	if int(target_list[4]) >= int(ref_list[4]):
		return True


def combine():
	# go to directory with data
	os.chdir("../../")
	os.chdir("data/combined/")
	# combined_file
	combined_file = "combined.csv"
	# check if file exists
	if os.path.isfile(combined_file):
		# return to directory
		os.chdir("../../")
		os.chdir("functions/combined/")
		pass
	else:
		# create the file 
		with open(combined_file, "w") as combined:
			# add the headers
			combined.write(",".join(headers_bus + headers_weather[8::1]) + "\n")
			# change directories
			os.chdir("../")
			os.chdir("weather/wunderground/")
			# iterate over weather
			with open("weather.csv", "r") as weather:
				counter = 0
				prior_list = weather.readline()
				counter += 1
				current_list = prior_list
				match = False
				# change directory
				os.chdir("../../")
				os.chdir("bus/insight/")
				# iterate over the entries in bus
				with open("bus.csv", "r") as bus:
					# skip first line
					bus.readline()
					# check each line of data in bus
					for bus_line in bus:
						bus_list = bus_line.strip().split(",")
						# skip blank entries
						if bus_list[0] == "":
							pass
						else:
							# go through weather until year, month, day, hour are matched
							match = check_match_hour(bus_list, current_list) # this line here to prevent skipping lines of the loop; data point might already be matched
							while match == False:
								line_data = weather_count(counter, weather, prior_list, current_list)
								counter = line_data[0]
								prior_list = line_data[1]
								current_list = line_data[2]
								match = check_match_hour(bus_list, current_list)
							# go through weather until prior is greatest lower bound by minute, current is equal or greater
							match = check_over_minute(bus_list, current_list) # this here in case already found the right pair
							while match == False:
								line_data = weather_count(counter, weather, prior_list, current_list)
								counter = line_data[0]
								prior_list = line_data[1]
								current_list = line_data[2]
								match = check_over_minute(bus_list, current_list)
							# see if the lower or upper bound is closer
							if abs(int(bus_list[4]) - int(prior_list[4])) < abs(int(bus_list[4]) - int(current_list[4])):
								combined.write(",".join(bus_list + prior_list[8::1]) + ",\n")
							else:
								combined.write(",".join(bus_list + current_list[8::1]) + ",\n")
			# return to the start
			os.chdir("../../../")
			os.chdir("functions/combined/")


def delete_sources():
	# change directory
	os.chdir("../../")
	os.chdir("data/bus/insight/")
	# remove bus
	os.remove("bus.csv")
	# change directory
	os.chdir("../../")
	os.chdir("weather/wunderground/")
	# remove weather
	os.remove("weather.csv")
	# change directory
	os.chdir("../../../")
	os.chdir("functions/combined/")


if __name__ == "__main__":
	combine()
	delete_sources()