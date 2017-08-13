# imports
import os
import glob


# directory changes
def quality_f_to_combined():
	os.chdir("../../")
	os.chdir("data/combined")

def combined_to_quality_f():
	os.chdir("../../")
	os.chdir("functions/quality")

def quality_f_to_quality_d():
	os.chdir("../../")
	os.chdir("data/combined/quality")

def quality_d_to_quality_f():
	os.chdir("../../../")
	os.chdir("functions/quality")


# file names
def file_names_in_directory(identifier):
	quality_to_combined()
	file_names = []
	for file_name in glob.glob(identifier):
		file_names.append(file_name)
	combined_to_quality()
	return file_names


def headers():
	# go to file
	quality_f_to_combined()
	# get the data
	with open("combined.csv", "r") as source:
		# back to start
		combined_to_quality_f()
		# return
		return source.readline().strip().split(",")

def header_index(title):
	# return
	return headers().index(title)


# UNIQUE VALUES
#create the storage files
def file_name_header_conversion():
	new_headers = []
	for header in headers():
		header = header.strip().split()
		new_header = ""
		for h in header:
			if h[0] != "(":
				new_header += h
		new_headers.append(new_header)
	return new_headers

def create_unique_value_files():
	new_headers = file_name_header_conversion()
	quality_f_to_quality_d()
	for h in new_headers:
		with open(h, "w") as destination:
			pass
	quality_d_to_quality_f()

def get_unique_values():
	file_names = file_name_header_conversion()
	uv_range = range(0, len(file_names), 1)
	quality_to_combined()
	with open("combined.csv", "r") as source:
		os.chdir("quality")
		source.readline()
		for line in source:
			line_list = line.strip().split(",")
			for i in uv_range:
				with open(file_names[i], "a") as destination:
					