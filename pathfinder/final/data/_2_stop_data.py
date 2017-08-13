# imports
import pickle



def get_pickle_file(file_name):
	f = open(file_name, "rb")
	python_data = pickle.load(f)
	f.close()
	return python_data

ctt_dict = get_pickle_file("ctt_dict.p")
for weekday in ctt_dict:
	for time_unit in ctt_dict[weekday]:
		for route in ctt_dict[weekday][time_unit]:
			print(weekday, time_unit, route)
			print(ctt_dict[weekday][time_unit][route])
			print("")