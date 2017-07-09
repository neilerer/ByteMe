# imports
import os
import glob
import headers


def create():
	# go to the directory with the source data
	os.chdir("../../")
	os.chdir("data/bus/insight/")
	# file_name
	file_name = "bus.csv"
	# files to use
	files_to_use = []
	for file in glob.glob("*.csv"):
		if file != file_name:
			files_to_use.append(file)
	# check if file exists
	if os.path.isfile(file_name):
		# return to staring directory
		os.chdir("../../../")
		os.chdir("functions/bus/")
		pass
	else:
		# create the file
		with open(file_name, "w") as destination:
			# add headers
			destination.write(",".join(headers.headers_clean) + "\n")
			# add the data from each file
			for file in files_to_use:
				with open(file, "r") as source:
					# skip the first line
					source.readline()
					# add the data
					for line in source:
						destination.write(line)
				# delete the source file
				os.remove(file)
		# return to staring directory
		os.chdir("../../../")
		os.chdir("functions/bus/")


if __name__ == "__main__":
	create()