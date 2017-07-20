# imports
import general


# JPI DICTIONARY
# Output: a diciontary where the keys are JPIs and the values are the associated bus stops in a list

# returns a dictionary with key of jpi and values of False (to be replaced with a list of the bus stops)
def skeleton_dictonary(bus_file_names_list):
	return {jpi:False for jpi in bus_file_names_list}

# creates a dicitonary with key of file name and values of associated bus stops
def file_name_dictionary():
	# a list with every bus stop file name in it
	file_name_list = general.list_of_bus_files()
	# a skeleton dictionary
	bus_stop_dict = skeleton_dictonary(file_name_list)
	# populate the skeleton dictionary with values: list of bust stops for the given jpi
	for file_name in bus_stop_dict:
		bus_stop_dict[file_name] = general.return_bus_stop_data(file_name)
	# return
	return bus_stop_dict

# converts a csv file name into a name reflectin only the jpi
def csv_file_name_to_name(file_name):
	return file_name.strip().split(".")[0]

# takes the return of file_name_dictionary and replaces full file name with just the jpi
def jpi_dictionary():
	bus_stop_dict = file_name_dictionary()
	for file_name in bus_stop_dict:
		name = csv_file_name_to_name(file_name)
		bus_stop_dict[name] = bus_stop_dict.pop(file_name)
	return bus_stop_dict

if __name__ == "__main__":
	my_dict = jpi_dictionary()
	print("jpi_dictionary")
	for item in my_dict:
		print(item)
		print(my_dict[item])
		print("")