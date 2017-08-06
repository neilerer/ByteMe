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
	os.chdir("data_json_review")
	# return
	return model_dict

def model_data_review_all_contents(model_dict):
	for weekday in model_dict:
		print(weekday)
		weekday_data = model_dict[weekday]
		for time_unit in weekday_data:
			print(time_unit)
			time_unit_data = weekday_data[time_unit]
			for stop in time_unit_data:
				print(stop)
				print(time_unit_data[stop])
				# stop : [(start, next, time, route), . . . ]

def model_data_review_number_of_stops(model_dict):
	# open the destination file
	destination = open("model_data_number_of_stops.txt", "w")
	# iterate over weekdays
	for weekday in model_dict:
		# record the weekday
		destination.write("Day of the Week: {}\n\n".format(weekday))
		# go into the weekday data
		weekday_data = model_dict[weekday]
		# iterate over time_units
		for time_unit in weekday_data:
			# record the time unit
			destination.write("Time Unit: {}\n".format(time_unit))
			# got into the time_unit data
			time_unit_data = weekday_data[time_unit]
			destination.write("Observations: {}\n\n".format(len(time_unit_data)))
		destination.write("\n\n\n\n")
	destination.close()

def model_data_review_stop_lengths(model_dict):
	# open the destination file
	destination = open("model_data_stop_lengths.txt", "w")
	# iterate over weekdays
	for weekday in model_dict:
		# record the weekday
		destination.write("Day of the Week: {}\n\n".format(weekday))
		# go into the weekday data
		weekday_data = model_dict[weekday]
		# iterate over time_units
		for time_unit in weekday_data:
			# record the time unit
			destination.write("Time Unit: {}\n".format(time_unit))
			# got into the time_unit data
			time_unit_data = weekday_data[time_unit]
			for stop in time_unit_data:
				stop_data = time_unit_data[stop]
				destination.write("{} has {} links\n\n".format(stop, len(stop_data)))
		destination.write("\n\n\n\n")
	destination.close()

if __name__ == "__main__":
	model_dict = get_model_data()
	model_data_review_number_of_stops(model_dict)
	model_data_review_stop_lengths(model_dict)