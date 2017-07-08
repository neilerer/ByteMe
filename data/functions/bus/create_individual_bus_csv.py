# imports
import os
import glob
from time import gmtime, strftime
import headers


# Timestamp
def utc_to_struct_time_list(utc):
	"""
	Description
	- converts a string representation of UTC into a struct_time format
	- will convert a single number into 8 unique entries

	Input
	utc: string representation of UTC
	- utc input value taken from the one dimensional array created by line_to_list()[0]

	Output
	utc: struct_time object
	https://docs.python.org/3/library/time.html#time.struct_time
	0: year
	1: month
	2: day
	3: hour
	4: minute
	5: second
	6: weekday; Monday == 0
	7: day of year
	8: daylight savings time: 0 no, 1 yes, -1 not known
	"""

	# convert to integer and divide by 1 million
	utc = int(utc) / 10**6
	# convert to struct_time
	utc = gmtime(utc)
	# does not return daylight savings time b/c not in the weather data
	return list(utc)[0:8:1]


def create_csv_clean():
	# go to the directory with the source data
	os.chdir("../../")
	os.chdir("data/bus/insight/")
	# identify the source files
	files_to_use = []
	for file in glob.glob("*_DB.csv"):
		files_to_use.append(file)
	# iterate over the source files
	for file in files_to_use:
		with open(file, "r") as source:
			# create a new file
			new_file = file[0:10:1] + ".csv"
			with open(new_file, "w") as destination:
				# add headers
				destination.write(",".join(headers.headers_clean) + "\n")
				# iterate over source to add data to destination
				for line in source:
					line_list = line.strip().split(",")
					time_list = utc_to_struct_time_list(line_list[0])
					new_list = [str(x) for x in time_list] + line_list
					destination.write(",".join(new_list) + "\n")
		# delete the old file
		os.remove(file)
	# return to the original directory
	os.chdir("../../../")
	os.chdir("functions/bus/")


if __name__ == "__main__":
	create_csv_clean()