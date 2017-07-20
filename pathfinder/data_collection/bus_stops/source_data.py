# imports
import os
import glob
import general


# JPI DICTIONARY
# Output: a diciontary where the keys are JPIs and the values are the associated bus stops
def skeleton_dictonary(bus_file_names_list):
	return {jpi:False for jpi in bus_file_names_list}

def file_name_dictionary():
	file_name_list = general.list_of_bus_files()
	bus_stop_dict = skeleton_dictonary(file_name_list)
	for file_name in bus_stop_dict:
		bus_stop_dict[file_name] = general.return_bus_stop_data(file_name)
	return bus_stop_dict

def csv_file_name_to_name(file_name):
	return file_name.strip().split(".")[0]

def jpi_dictionary():
	bus_stop_dict = file_name_dictionary()
	for file_name in bus_stop_dict:
		file_name = csv_file_name_to_name(file_name)
	return bus_stop_dict


my_dict = jpi_dictionary()
print("jpi_dictionary")
for item in my_dict:
	print(item)
	print(my_dict[item])
	print("")