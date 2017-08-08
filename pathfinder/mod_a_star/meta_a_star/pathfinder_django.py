# imports pathfinder
import data
import pathfinder



def weekday_list(model_dict):
	wd_list = list()
	for weekday in model_dict:
		wd_list.append(weekday)
	return wd_list

def time_unit_list(wd_list, model_dict):
	tu_list = set()
	for weekday in wd_list:
		for time_unit in model_dict[weekday]:
			tu_list.add(time_unit)
	return list(tu_list)



def check_weekday(weekday, model_dict):
	if weekday in model_dict:
		return True
	else:
		return False

def enter_correct_weekday(model_dict):
	correct = False
	while not correct:
		try:
			weekday = int(input("Enter a weekday: "))
			correct = check_weekday(weekday, model_dict)
		except:
			Print("Please try another weekday; the one you entered does not exist.")



def check_time_unit(weekday, time_unit, model_dict):
	if time_unit in model_dict[weekday]:
		return True
	else:
		return False

def enter_correct_time_unit(weekday, model_dict):
	correct = False
	while not correct:
		try:
			time_unit = int(input("Enter a time_unit: "))
			correct = check_time_unit(weekday, time_unit, model_dict)
		except:
			print("Please try another time_unit; the one you entered does not exist.")
	return time_unit



def check_stop_id(weekday, time_unit, model_dict, stop_id):
	time_unit_dict = model_dict[weekday][time_unit]
	if stop_id in time_unit:
		return True
	else:
		return False

def enter_correct_stop_id(weekday, time_unit, model_dict):
	correct = False
	while not correct:
		try:
			stop_id = input("Enter a starting stop id: ")
			correct = check_stop_id(weekday, time_unit, model_dict, stop_id)
		except:
			Print("Please try another stop id; the one you entered does not exist.")
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
	# return
	return django_journey



def run_the_pathfinder():
	# welcome message
	print("ByteMe's pathfindr is now running, so give it a go.")
	# data
	model_dict = data.get_model_data()
	connections_dict = data.get_connections_dict()
	# the operational component
	running = True
	while running:
		# user inputs
		weekday = enter_correct_weekday(model_dict)
		time_unit = enter_correct_time_unit(weekday, model_dict)
		start_stop_id = enter_correct_stop_id(weekday, time_unit, model_dict, stop_id_dict)
		end_stop_id = enter_correct_stop_id(weekday, time_unit, model_dict, stop_id_dict)
		# pathfinder
		the_shortest_journey = pathfinder.pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict, connections_dict)
		print("Here is the suggested bus journey")
		print(pathfinder_for_django(the_shortest_journey))



if __name__ == "__main__":
	# run_the_pathfinder()



	model_dict = data.get_model_data()
	wd_list = weekday_list(model_dict)
	tu_list = time_unit_list(wd_list, model_dict)
	print(wd_list)
	print(tu_list)