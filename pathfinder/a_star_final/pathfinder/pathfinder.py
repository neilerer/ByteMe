# imports
import data
import a_star



def pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict):
	journey_id_list = list()
	journies_dict = dict()
	been_set = set()
	the_shortest_journey = a_star.a_star(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
	return the_shortest_journey



def pathfinder_for_django(the_shortest_journey):
	# unpack the data
	journey_time = the_shortest_journey[0]
	journey_details = the_shortest_journey[1]
	# tabulation data
	route_list = list()
	stop_list = list()
	time_list = list()
	# iterate over journey_details
	for quadruple in journey_details:
		# unpack
		current_stop = quadruple[0]
		next_stop = quadruple[1]
		time = quadruple[2]
		route = quadruple[3]
		# set the index
		if route not in route_list:
			# create objects if they don't exist
			route_list.append(route)
			stop_list.append(list())
			time_list.append(0.00)
		index = route_list.index(route)
		# add the stops
		route_in_stop_list = stop_list[index]
		# determine if the current stop should be recorded
		try:
			if current_stop != route_in_stop_list[-1]:
				route_in_stop_list.append(current_stop)
		except:
			route_in_stop_list.append(current_stop)
		# record the next stop
		route_in_stop_list.append(next_stop)
		# update the time
		time_list[index] += time
	# return
	pathfinder_dict = dict()
	for route in route_list:
		index = route_list.index(route)
		pathfinder_dict[route] = [time_list[index], stop_list[index]]
	return pathfinder_dict



if __name__ == "__main__":
	# data
	print("Loading the model data . . .")
	model_dict = data.get_model_data()

	# inputs
	start_stop_id =  4486
	end_stop_id = 400
	weekday = 0
	time_unit = 10

	# test pathfinder
	print("")
	print("Pathfinder")
	the_shortest_journey = pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict)
	print(the_shortest_journey)
	for item in the_shortest_journey[1]:
		print(item)
	print("")

	# test pathfinder_for_django
	print("")
	print("Pathfinder for Django")
	print(pathfinder_for_django(the_shortest_journey))
	print("")