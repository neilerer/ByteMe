# imports
import pickle



def get_pickle_file(file_name):
	f = open(file_name, "rb")
	python_data = pickle.load(f)
	f.close()
	return python_data



def review_file(file_name):
	pickle_file = get_pickle_file(file_name)
	for weekday in pickle_file:
		for time_unit in pickle_file[weekday]:
			for route in pickle_file[weekday][time_unit]:
				print(weekday, time_unit, route)
				print(pickle_file[weekday][time_unit][route])
				print("")