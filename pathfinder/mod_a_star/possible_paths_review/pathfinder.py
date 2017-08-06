# imports
import os
import glob
import pickle


def sp_to_pp():
	os.chdir("../")
	os.chdir("possible_paths")

def pp_to_sp():
	os.chdir("../")
	os.chdir("shortest_path")



def get_time_unit_path_dict_by_units(weekday, time_unit):
	key = str(weekday) + "_" + str(time_unit)
	file_name = key + ".p"
	sp_to_pp()
	f = open(file_name, "rb")
	time_unit_path_dict = pickle.load(f)
	f.close()
	pp_to_sp()
	return [key, time_unit_path_dict]



def get_time_unit_path_dict_by_file_name(file_name):
	sp_to_pp()
	f = open(file_name, "rb")
	time_unit_path_dict = pickle.load(f)
	f.close()
	pp_to_sp()
	key = file_name.strip().split(".")[0]
	return [key, time_unit_path_dict]



def time_unit_path_dict_review(weekday, time_unit):
	# {'0_7': {('00590', '00590'): {0: ['00590']}, ('00590', '01111'): {0: ['00590', '01111']}, ('00590', '045A0'): {1: ['00590', '045A0']}, ('00590', '00070'): {2: ['00590', '00070']}, ('00590', '00080'): {3: ['00590', '00080']}, ('00590', '00081'): {4: ['00590', '00081']}
	source = get_time_unit_path_dict(weekday, time_unit)
	key = source[0]
	time_unit_path_dict = source[1]

	time_unit_dict = time_unit_path_dict[key]

	for path_id in time_unit_dict:
		path = time_unit_dict[path_id]
		print(path_id)
		print(path)
		print("")



def get_time_unit_path_dict_file_names():
	sp_to_pp()
	file_name_list = list()
	for file_name in glob.glob("*.p"):
		if file_name[1] == "_":
			file_name_list.append(file_name)
	pp_to_sp()
	return file_name_list



if __name__ == "__main__":
	file_name_list = get_time_unit_path_dict_file_names()
	for file_name in file_name_list:
		print(file_name)