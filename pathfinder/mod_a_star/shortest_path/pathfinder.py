# imports
import os
import pickle



def get_time_unit_path_dict(weekday, time_unit):
	file_name = str(weekday) + "_" + str(time_unit) + ".p"
	os.chdir("../")
	os.chdir("possible_paths")
	f = open(file_name, "rb")
	time_unit_path_dict = pickle.load(f)
	f.close()
	os.chdir("../")
	os.chdir("shortest_path")
	return time_unit_path_dict



time_unit_path_dict = get_time_unit_path_dict(0, 7)
for item in time_unit_path_dict:
	print(item)