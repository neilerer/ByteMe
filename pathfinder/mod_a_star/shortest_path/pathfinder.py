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
		try:
			if int(file_name[0]):
				file_name_list.append(file_name)
		except:
			pass
	pp_to_sp()
	return file_name_list



def combine_time_unit_path_dicts():
	time_unit_path_dicts = dict()
	file_name_list = get_time_unit_path_dict_file_names()
	for file_name in file_name_list:
		new_items = get_time_unit_path_dict_by_file_name(file_name)
		key = new_items[0]
		time_unit_path_dict = new_items[1]
		time_unit_path_dicts[key] = time_unit_path_dict
	return time_unit_path_dicts



def combined_time_unit_path_dicts_to_file():
	time_unit_path_dicts = combine_time_unit_path_dicts()
	destination = open("time_unit_path_dicts" + ".p", "wb")
	pickle.dump(time_unit_path_dicts, destination)
	destination.close()



if __name__ == "__main__":
	combine_time_unit_path_dicts()