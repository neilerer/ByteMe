# imports
import os
import glob
import wd_headers
import wd_functions


"""
These functions convert the original weather files into clean files
Note: the orignal files are deleted after a clean file is create (economics of storage)
"""


def get_headers(file_name):
	return wd_functions.csv_line_to_list(file_name.readline())

def create_new_file_name(file_name):
	return file_name.split(".")[0] + ".csv"

def headers_index_raw(headers_old_list):
	header_index = []
	for header in wd_headers.raw:
		header_index.append(headers_old_list.index(header))
	return header_index

def refine_old_list(old_list, index):
	refined_old_list = []
	for i in index:
		refined_old_list.append(old_list[i])
	return refined_old_list

def clean_list(old_list):
	# create the return object
	clean_list = []
	# populate clean_list
	clean_list.append(wd_functions.wd_hour(old_list[0]))
	clean_list.append(wd_functions.wd_minute(old_list[0]))
	clean_list.append(wd_functions.wd_temp(old_list[1]))
	clean_list.append(wd_functions.wd_temp(old_list[2]))
	clean_list.append(wd_functions.wd_humidity(old_list[3]))
	clean_list.append(wd_functions.wd_pressure(old_list[4]))
	clean_list.append(wd_functions.wd_visibility(old_list[5]))
	clean_list.append(wd_functions.wd_wind_direction(old_list[6]))
	clean_list.append(wd_functions.wd_wind_speed(old_list[7]))
	clean_list.append(wd_functions.wd_gust_speed(old_list[8]))
	clean_list.append(wd_functions.wd_precipitation(old_list[9]))
	clean_list.append(wd_functions.wd_events(old_list[10]))
	clean_list.append(wd_functions.wd_condition(old_list[11]))
	# return clean_list
	return clean_list


def individual_files():
	# go to the directory with the source data
	os.chdir("../../")
	os.chdir("data/weather/wunderground/")
	# iterate over the files
	for file_name_old in glob.glob("*.wun.csv"):
		# create a new file name
		file_name_new = create_new_file_name(file_name_old)
		# create new file
		with open(file_name_new, "w") as new_file:
			# add the new headers
			new_file.write(",".join(wd_headers.clean) + "\n")
			# open old file
			with open(file_name_old, "r") as old_file:
				# get the old headers
				headers_old = get_headers(old_file)
				# find where the headers we want are located
				header_index = headers_index_raw(headers_old)
				# convert each line into final form
				for line in old_file:
					# refined list of raw content
					old_list = wd_functions.csv_line_to_list(line)
					old_list = refine_old_list(old_list, header_index)
					# make new_list
					if old_list[0] == '':
						pass
					else:
						new_file.write(",".join(clean_list(old_list)) + "\n")
			# delete the old file; we don't have much storage
			os.remove(file_name_old)
	# return to functions
	os.chdir("../../../")
	os.chdir("functions/weather")


if __name__ == "__main__":
	individual_files()