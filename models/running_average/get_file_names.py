# imports
import glob



def all_csv():
	# create the list
	file_name_list = list()
	# iterate over .csv files
	for file_name in glob.glob("*.csv"):
		length = len(file_name)
		name = file_name[0:length - 5]
		file_name_list.append(name)
	return file_name_list