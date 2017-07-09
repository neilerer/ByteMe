# imports
import os
import glob
import headers


"""
These functions take the raw JourneyPatternID files and transforms them into containing only the features desired
Note: after a reduced file is made, the raw file is deleted (economics of storage)
"""


# global variables
headers_list = headers.headers
headers_reduced_list = headers.headers_reduced
utc_index = headers_reduced_list.index("Timestamp")


# utility functions
def jpif_to_jpid():
	os.chdir("../../")
	os.chdir("data/JourneyPatternID")

def jpid_to_jpif():
	os.chdir("../../")
	os.chdir("functions/JourneyPatternID")


# dimention reduction
def jpi_reduce_individual(file_name):
	# new file name
	file_name_new = file_name.split(".")[0] + "reduced.csv"
	# header mapping
	headers_mapping = [headers_list.index(h) for h in headers_reduced_list]
	# create a new file
	with open(file_name_new, "w") as destination:
		# open the source file
		with open(file_name, "r") as source:
			# populate destination
			for line in source:
				line_list = line.strip().split(",")
				new_list = [line_list[x] for x in headers_mapping]
				# convert utc values into proper utc value
				if new_list[utc_index] == "Timestamp":
					pass
				else:
					new_list[utc_index] = new_list[utc_index][:-6]
				destination.write(",".join(new_list) + "\n")


def jpi_reduction_source_files():
	# create list to contain source files
	csv_files = []
	# add all csv files
	for file in glob.glob("*csv"):
		csv_files.append(file)
	# sort source_files
	csv_files.sort()
	# make sure no redundant files are included
	source_files = []
	count = 0
	count_bound = len(csv_files)
	while count < count_bound - 1:
		if csv_files[count][0:8:1] == csv_files[count + 1][0:8:1]:
			count += 2
		elif csv_files[count][-1:-6:-1] == "vsc.d":
			count += 1
		else:
			source_files.append(csv_files[count])
			count += 1
	if (csv_files[-1] not in source_files) and (csv_files[-1][-1:-6:-1] != "vsc.d"):
		source_files.append(csv_files[-1])
	# return
	return source_files


def jpi_reduce_all():
	# change directory
	jpif_to_jpid()
	# define the source files
	source_files = jpi_reduction_source_files()
	# create the reduced files
	for file in source_files:
		jpi_reduce_individual(file)
		os.remove(file)
	# change directory
	jpid_to_jpif()

if __name__ == "__main__":
	jpi_reduce_all()

# #testing just one file for development
# jpif_to_jpid()
# jpi_reduce_individual("00010002.csv")
# jpid_to_jpif()