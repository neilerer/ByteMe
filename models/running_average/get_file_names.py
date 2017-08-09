# imports
import glob



def all_csv():
	# create the list
	file_name_list = list()
	# iterate over .csv files
	for file_name in glob.glob("*.csv"):
		length = len(name)
		name = file_name[0:length - 6]
		file_name_list.append(name)
	return file_name_list