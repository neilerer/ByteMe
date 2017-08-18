# imports
import os



def number_of_observations():
	# go to directory with data
	os.chdir("../../")
	os.chdir("data/combined/")
	# open the file
	count = 0
	with open("combined.csv") as source:
		for line in source:
			count += 1
	# return to the start
	os.chdir("../../../")
	os.chdir("functions/combined/")
	# return
	return count - 1

def number_of_features():
	# go to directory with data
	os.chdir("../../")
	os.chdir("data/combined/")
	# open the file
	length = 0
	with open("combined.csv") as source:
		length = len(source.readline().strip().split())
	# return to the start
	os.chdir("../../../")
	os.chdir("functions/combined/")
	# return
	return length



if __name__ == "__main__":
	n_o = number_of_observations()
	n_f = number_of_features()
	print("Summary of combined.csv")
	print("There are {} observations".format(n_o))
	print("There are {} features".format(n_f))
	pritn("There are {} data points".format(n_o * n_f))