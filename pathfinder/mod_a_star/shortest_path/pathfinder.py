# imports
import os
import glob
import pickle



def get_time_unit_path_dict(weekday, time_unit):
	key = str(weekday) + "_" + str(time_unit)
	file_name = key + ".p"
	os.chdir("../")
	os.chdir("possible_paths")
	f = open(file_name, "rb")
	time_unit_path_dict = pickle.load(f)
	f.close()
	os.chdir("../")
	os.chdir("shortest_path")
	return [key, time_unit_path_dict]


# {'0_7': {('00590', '00590'): {0: ['00590']}, ('00590', '01111'): {0: ['00590', '01111']}, ('00590', '045A0'): {1: ['00590', '045A0']}, ('00590', '00070'): {2: ['00590', '00070']}, ('00590', '00080'): {3: ['00590', '00080']}, ('00590', '00081'): {4: ['00590', '00081']}

def time_unit_path_dict_review(weekday, time_unit):
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
	os.chdir("../")
	os.chdir("possible_paths")
	file_name_list = list()
	for file_name in glob.glob("*.p"):
		try:
			if int(file_name[0]):
				file_name_list.append(file_name)
		except:
			pass
	os.chdir("../")
	os.chdir("shortest_path")
	return file_name_list

print(get_time_unit_path_dict_file_names())