# imports
import os
import glob
import datetime
import wd_headers
import wd_functions


# Date and Time
def date_elements(file_name):
	# [Year, Month, Day]
	return file_name.split(".")[0].split("_")


def datetime_list(date, time):
	output = date + time
	output = datetime.datetime(*map(int, output))
	# returns: [Year, Month, Day, Hours, Minute, Second, Day of the Week (Monday == 0), Day of the Year (0 to 366)]
	return [int(x) for x in output.strftime("%Y %m %d %H %M %S %w %j").split(" ")]


def create_weather():
	# weather file
	weather_file = "weather.csv"
	# go to the directory with the source data
	os.chdir("../../")
	os.chdir("data/weather/wunderground/")
	# check if file already exists
	if os.path.isfile(weather_file):
		pass
	else:
		# create the file
		with open(weather_file, "w") as clean:
			# instantiate the counter
			counter = 0
			# add the headers
			headers_csv_line = ",".join(wd_headers.final)
			clean.write(headers_csv_line + "\n")
			# increment the counter
			counter += 1
			# create prior_list
			prior_list = wd_headers.final
			# iterate over the data files
			for file_name in glob.glob("*.csv"):
				# prevent infinite loop
				if file_name != weather_file:
					# open the file
					with open(file_name, "r") as source_file:
						# get the date
						date = date_elements(file_name)
						# skip the first line
						source_file.readline()
						# get the data
						for line in source_file:
							# extract the existing data
							line_list = wd_functions.csv_line_to_list(line)
							# create the desired datetime elements
							time = line_list[0:2:1]
							dt_list = [str(x) for x in datetime_list(date, time)]
							# new_line_list
							new_line_list = dt_list + line_list[2::1]
							# compare new_line_list to prior_list
							if new_line_list[0:5:1] == prior_list[0:5:1]:
								pass
							else:
								# csv_line
								csv_line = ",".join(new_line_list)
								# add to the new file
								clean.write(csv_line + "\n")
							prior_list = new_line_list
					# remove the old file; we don't have much storage
					os.remove(file_name)
				else:
					pass
	# return to functions
	os.chdir("../../../")
	os.chdir("functions/weather")


if __name__ == "__main__":
	create_weather()