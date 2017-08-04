# imports
import os
import pickle



def get_model_data():
	# change directory
	os.chdir("../")
	os.chdir("data_json")
	# get shit from file
	f = open("data.p", "rb")
	# load the pickle file
	model_dict = pickle.load(f)
	# close the pickle file
	f.close()
	# change directory
	os.chdir("../")
	os.chdir("data_linked_list")
	# return
	return model_dict

def model_data_review(model_dict):
	for weekday in model_data:
		print(weekday)
		weekday_data = model_data[weekday]
		for time_unit in weekday_data:
			print(time_unit)
			time_unit_data = weekday_data[time_unit]
			print(len(time_unit_data))
			# for stop in time_unit_data:
			# 	print(stop)
			# 	print(time_unit_data[stop])
			# 	# stop : [(start, next, time, route), . . . ]

model_dict = get_model_data()
model_data_review(model_dict)


def dict_to_list(model_data):
	triple_list = list()
	for weekday in model_data:
		weekday_data = model_data[weekday]
		temp_triple_list = list()
		for jpi in weekday_data:
			jpi_data = weekday_data[jpi]
			for stop in jpi_data:
				time = jpi_data[stop]
				triple = (stop, jpi, time)
				temp_triple_list.append(triple)
			triple_list.append(temp_triple_list)
	return triple_list

def dict_to_list_review(triple_list):
	for jpi_list in triple_list:
		print(jpi_list)
		print("")


# triple_list = dict_to_list(model_data)
# dict_to_list_review(triple_list)



def linked_list_element_creation(route_list, index_prior, index_current):
	# prior information
	prior_triple = route_list[index_prior]
	prior_stop = prior_triple[0]
	prior_route = prior_triple[1]
	prior_time = prior_triple[2]
	# current information
	current_triple = route_list[index_current]
	current_stop = current_triple[0]
	current_route = current_triple[1]
	current_time = current_triple[2]
	# return
	return (prior_stop, (prior_stop, prior_route, current_stop, current_time - prior_time))

def triple_list_to_linked_list(triple_list):
	stop_linked_list = dict()
	for route_list in triple_list:
		length = len(route_list)
		for i in range(1, length, 1):
			index_prior = i - 1
			index_current = i
			linked_list_element = linked_list_element_creation(route_list, index_prior, index_current)
			stop_id = linked_list_element[0]
			stop_linked_list_element = linked_list_element[1]
			if stop_id in stop_linked_list:
				stop_linked_list[stop_id].append(stop_linked_list_element)
			else:
				stop_linked_list[stop_id] = [stop_linked_list_element]
	return stop_linked_list

def linked_list_review(stop_linked_list):
	for stop_route_id in stop_linked_list:
		print(stop_route_id)
		print(stop_linked_list[stop_route_id])
		print("")



def linked_list_for_export():
	model_data = general.test_data_from_file()
	triple_list = dict_to_list(model_data)
	stop_linked_list = triple_list_to_linked_list(triple_list)
	return stop_linked_list

# if __name__ == "__main__":
# 	model_data = get_model_data()
# 	triple_list = dict_to_list(model_data)
# 	stop_linked_list = triple_list_to_linked_list(triple_list)
# 	linked_list_review(stop_linked_list)