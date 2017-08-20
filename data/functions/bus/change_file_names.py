# imports
import os
import glob


"""
Purpose: change the names of the raw bus files
Input: none
Output: none
Effect: file names will be changed and ready for use by other programs
"""
def change_file_names():
	# go to the directory with the source data
	os.chdir("../../")
	os.chdir("data/bus/insight/")
	# iterate over the files
	files_to_change = []
	for file in glob.glob("siri*.csv"):
		files_to_change.append(file)
	for file in files_to_change:
		new_name = "_".join([file[0:4:1], file[5:7:1], file[8:10:1], "DB.csv"])
		os.rename(file, new_name)
	# return to the original directory
	os.chdir("../../../")
	os.chdir("functions/bus/")


# run the program
if __name__ == "__main__":
	change_file_names()