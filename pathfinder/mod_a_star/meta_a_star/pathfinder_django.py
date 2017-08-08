# imports pathfinder
import data
import pathfinder



def weekday_list():
	model_dict = data.get_model_data()
	wd_list = list()
	for weekday in model_dict:
		wd_list.append(weekday)
	return wd_list

def time_unit_list(wd_list):
	model_dict = data.get_model_data()
	tu_list = set()
	for weekday in wd_list:
		for time_unit in model_dict[weekday]:
			tu_list.add(time_unit)
	return list(tu_list)

def stop_id_dict():
	model_dict = data.get_model_data()
	stop_id_dict = dict()
	for weekday in model_dict:
		stop_id_dict[weekday] = dict()
		for time_unit in model_dict[weekday]:
			stop_id_dict[weekday][time_unit] = list()
			for stop_id in model_dict[weekday][time_unit]:
				stop_id_dict[weekday][time_unit].append(stop_id)
	return stop_id_dict



def enter_correct_value_from_list(value_list, input_message, except_message):
	correct = False
	while not correct:
		try:
			value = int(input(str(input_message)))
			correct = value in value_list
		except:
			print(except_message)
	return value



def check_stop_id(weekday, time_unit, stop_id, si_dict):
	time_unit_dict = si_dict[weekday][time_unit]
	if stop_id in time_unit_dict:
		return True
	else:
		return False

def enter_correct_stop_id(weekday, time_unit, si_dict):
	correct = False
	while not correct:
		try:
			stop_id = int(input("Enter a starting stop id: "))
			correct = check_stop_id(weekday, time_unit, stop_id, si_dict)
		except:
			print("I'm sorry, the stop id you entered is invalid.")
	return stop_id



def pathfinder_for_django(the_shortest_journey):
	# unpack the data
	journey_time = the_shortest_journey[0]
	journey_details = the_shortest_journey[2]
	# generate a stop_id_journey
	django_journey = dict()
	for quadruple in journey_details:
		# unpack the data
		start_stop = quadruple[0]
		time = quadruple[2]
		route = quadruple[3]
		# populate django_journey
		if route in django_journey:
			django_journey[route][0] += time
			django_journey[route][1].append(start_stop)
		else:
			django_journey[route] = [time, [start_stop]]
	# add the last stop
	last_stop_data = journey_details[-1]
	ls_route = last_stop_data[3]
	ls_stop = last_stop_data[1]
	django_journey[ls_route].append(ls_stop)
	# return
	return django_journey



def run_the_pathfinder():
	# data
	print("")
	print("")
	print("Generating and loading weekday list to memory . . . ")
	wd_list = weekday_list()
	print("Generating and loading time_unit list to memory . . . ")
	tu_list = time_unit_list(wd_list)
	print("Generating and loading stop_id dictionary to memory . . . ")
	si_dict = stop_id_dict()
	print("Loading the model_dict to memory . . . ")
	model_dict = data.get_model_data()
	print("Loading the connections_dict to memory . . . ")
	connections_dict = data.get_connections_dict()
	# the operational component
	running = True
	while running:
		# welcome
		print("")
		print("The pathfinder is ready to use.")
		# user inputs
		weekday = enter_correct_value_from_list(wd_list, "Please enter a weekday: ", "I'm sorry, that is invalid weekday.")
		time_unit = enter_correct_value_from_list(tu_list, "Please enter a time_unit: ", "I'm sorry, that is invalid time_unit.")
		start_stop_id = enter_correct_stop_id(weekday, time_unit, si_dict)
		end_stop_id = enter_correct_stop_id(weekday, time_unit, si_dict)
		# pathfinder
		the_shortest_journey = pathfinder.pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict, connections_dict)
		print("Here is the suggested bus journey")
		print(pathfinder_for_django(the_shortest_journey))
		print("")



if __name__ == "__main__":
	run_the_pathfinder()