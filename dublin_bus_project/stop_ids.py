# imports
import os
import pickle
import data
import shortest_journey



# data
model_dict = data.get_model_data()



def time_unit_dict(weekday, time_unit, model_dict):
	return shortest_journey.time_unit_model_dict(weekday, time_unit, model_dict)



def stop_ids(model_dict):
	# this loads fast enough that we should just load it into memory and only store model_dict on django
	stop_id_dict = dict()
	for weekday in model_dict:
		stop_id_dict[weekday] = dict()
		for time_unit in model_dict[weekday]:
			stop_id_dict[weekday][time_unit] = list()
			for stop_id in model_dict[weekday][time_unit]:
				stop_id_dict[weekday][time_unit].append(stop_id)
	return stop_id_dict



def stop_ids_to_file(model_dict):
	# get shit to file
	stop_id_dict = stop_ids(model_dict)
	os.chdir("../")
	os.chdir("data")
	destination = open("stop_id_dict.p", "wb")
	# dump the data into the pickle file
	pickle.dump(stop_id_dict, destination)
	# close the file
	destination.close()
	os.chdir("../")
	os.chdir("pathfinder")



if __name__ == "__main__":
	stop_ids_to_file(model_dict)