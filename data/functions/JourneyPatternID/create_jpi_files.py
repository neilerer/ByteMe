# imports
import os
import glob


"""
These functions are used to extract and save information from the combined csv file and regroup it by JourneyPatternID
"""


# directory functions
def jpif_to_combined():
	os.chdir("../../")
	os.chdir("data/combined")

def combined_to_jpid():
	os.chdir("../JourneyPatternID")

def combined_to_jpif():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")

def jpif_to_jpid():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")

def jpid_to_jpif():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")


"""
This function creates an array of the unique jpis
"""
def unique_journey_pattern_ids():
	# create the return object
	ujpi_set = set()
	# go to directory
	jpif_to_combined()
	# open the source
	with open("combined.csv", "r") as source:
		# define the headers
		headers = source.readline().strip().split(",")
		# find the location of the jpi
		offset = headers.index("JourneyPatternID")
		# iterate over the data in the file
		for line in source:
			try:
				# if one exists, add the jpi to the set
				jpi = line.strip().split(",")[offset]
				if jpi == "" or jpi == None:
					pass
				else:
					ujpi_set.add(jpi)
			except:
				# otherwise, pass
				pass
	# return to the starting directory
	combined_to_jpif()
	# return
	return [ujpi_set, headers]


"""
This function creates a file for each jpi
"""
def create_destination_files():
	# data
	data = unique_journey_pattern_ids()
	# obtain the unique jpis
	unique_journey_pattern_id_list = data[0]
	headers = data[1]
	# go to the directory
	jpif_to_jpid()
	# iteratively create the jpis
	for ujpi in unique_journey_pattern_id_list:
		# create the file
		with open(ujpi + ".csv", "w") as source:
			# write the header
			source.write(",".join(headers) + "\n")
	# return to the starting point
	jpid_to_jpif()



"""
This function populates each jpi file by accessing the the source information from the combined data file
"""
def populate_jpi_data():
	# change directories
	jpif_to_combined()	
	# open source
	with open("combined.csv", "r") as source:
		# create headers
		headers = source.readline().strip().split(",")
		# create index variables
		timestamp_index = headers.index("Timestamp")
		jpi_index = headers.index("JourneyPatternID")
		as_index = headers.index("AtStop")
		# change directory
		combined_to_jpid()
		# add to each existing file
		for line in source:
			try:
				# line into a list
				line_list = line.strip().split(",")
				# variable to open the apprpriate file
				jpi = line_list[jpi_index]
				# modify the timestampt so that in future it will not need to be divided by 10**6
				line_list[timestamp_index] = str(int(int(line_list[timestamp_index]) / 10**6))
				# define destination file
				destination_file = jpi + ".csv"
				# open the destination file
				# note: would be quicker to keep all files open, but in some cases this might eat up too much memory
				# note: as this is a one-off run, run-time minimisation is not a priority, but crashing a computer is a concern
				with open(destination_file, "a") as destination:
					# write to the file
					destination.write(",".join(line_list) + "\n")
			except:
				# the line did not have the data
				pass
	# return to the starting directory
	jpid_to_jpif()


"""
Run the program
"""
if __name__ == "__main__":
	create_destination_files()
	populate_jpi_data()