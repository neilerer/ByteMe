# imports
import data
import dijkstra



def pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict):
	journey_id_list = list()
	journies_dict = dict()
	been_set = set()
	the_shortest_journey = dijkstra.dijkstra(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
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
		route_time = time_list[index]
		route_time += time
	# return
	pathfinder_dict = dict()
	for route in route_list:
		index = route_list.index(route)
		pathfinder_dict[route] = [time_list[index], stop_list[index]]
	return pathfinder_dict



# def pathfinder_for_django(the_shortest_journey):
# 	# unpack the data
# 	journey_time = the_shortest_journey[0]
# 	journey_details = the_shortest_journey[1]
# 	# generate a stop_id_journey
# 	django_journey = dict()
# 	# instantiate prior data
# 	prior_quadruple = journey_details[0]
# 	prior_start = prior_quadruple[0]
# 	prior_end = prior_quadruple[1]
# 	prior_time = prior_quadruple[2]
# 	prior_route = prior_quadruple[3]
# 	# iterate over journey_details
# 	for quadruple in journey_details:
# 		# unpack the data
# 		start_stop = quadruple[0]
# 		end_stop = quadruple[1]
# 		time = quadruple[2]
# 		route = quadruple[3]
# 		# route change event
# 		if route != prior_route:
# 			django_journey[prior_route][1].append(prior_end)
# 		# regular updates
# 		if route in django_journey:
# 			django_journey[route][0] += time
# 			django_journey[route][1].append(start_stop)
# 		else:
# 			django_journey[route] = [time, [start_stop]]
# 		# update priors
# 		prior_start = start_stop
# 		prior_end = end_stop
# 		prior_time = time
# 		prior_route = route
# 	# add the last stop to the last segement
# 	last_stop_data = journey_details[-1]
# 	ls_route = last_stop_data[3]
# 	ls_stop = last_stop_data[1]
# 	django_journey[ls_route][1].append(ls_stop)
# 	# return
# 	return django_journey




if __name__ == "__main__":
	# data
	print("Loading the model data . . .")
	model_dict = data.get_model_data()

	# inputs
	start_stop_id =  807
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