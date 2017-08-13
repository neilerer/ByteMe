# imports
import data
import pathfinder



def time_unit_model_dict(weekday, time_unit, model_dict):
	# time_unit_dict
	return model_dict[weekday][time_unit]

def destination_routes(end_stop_id, weekday, time_unit, model_dict):
	destination_route_list = list()
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	for quadruple in time_unit_dict[end_stop_id]:
		route = quadruple[3]
		destination_route_list.append(route)
	return destination_route_list

def take_this_route(q_start_stop_id, end_stop_id, weekday, time_unit, route, model_dict):
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	list_of_quadruples = list()
	arrived = False
	while not arrived:
		quadruples_of_interest = time_unit_dict[q_start_stop_id]
		the_quadruple = None
		for quadruple in quadruples_of_interest:
			if quadruple[3] == route:
				the_quadruple = quadruple
				break
		list_of_quadruples.append(the_quadruple)
		if the_quadruple[1] == end_stop_id:
			arrived = True
			return list_of_quadruples
		else:
			q_start_stop_id = the_quadruple[1]

def minimum_transfers(the_shortest_journey, destination_route_list, start_stop_id, end_stop_id, weekday, time_unit, model_dict):
	shortest_journey_with_minimum_transfers = list()
	for quadruple in the_shortest_journey[1]:
		# unpacking
		q_start_stop_id = quadruple[0]
		q_end_stop_id = quadruple[1]
		journey_time  =quadruple[2]
		route = quadruple[3]
		# the condition
		if route not in destination_route_list:
			shortest_journey_with_minimum_transfers.append(quadruple)
		else:
			last_quadruples = take_this_route(q_start_stop_id, end_stop_id, weekday, time_unit, route, model_dict)
			for lq in last_quadruples:
				shortest_journey_with_minimum_transfers.append(lq)
			return shortest_journey_with_minimum_transfers



def output_for_django(sj_list):
	journey_dict = dict()
	route_dict = dict()
	current_route = None
	for quadruple in sj_list:
		# print(quadruple)
		# unpack
		start = quadruple[0]
		end = quadruple[1]
		travel  =quadruple[2]
		route = quadruple[3]
		if route == current_route:
			pass
		else:
			current_route = route
			if route in route_dict:
				route_dict[route] += 1
			else:
				route_dict[route] = 1
		key = "{} Trip {}".format(route, str(route_dict[route]))
		# 
		if key in journey_dict:
			journey_dict[key][0] += travel
			journey_dict[key][1].append(end)
		else:
			journey_dict[key] = [0.0, None]
			journey_dict[key][0] = travel
			journey_dict[key][1] = [start, end]
	# return
	return journey_dict



if __name__ == "__main__":
	# data
	print("Loading the model data . . .")
	model_dict = data.get_model_data()

	# inputs
	start_stop_id =  807
	end_stop_id = 763
	weekday = 0
	time_unit = 10

	# destination_roue_list
	destination_route_list = destination_routes(end_stop_id, weekday, time_unit, model_dict)

	# test pathfinder
	print("")
	print("")
	print("Minimum Time")
	the_shortest_journey = pathfinder.pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict)
	for quadruple in the_shortest_journey[1]:
		print(quadruple)
	print("")

	# test minimum_transfers
	print("")
	print("Minimum Transfers")
	min_trans = minimum_transfers(the_shortest_journey, destination_route_list, start_stop_id, end_stop_id, weekday, time_unit, model_dict)
	for quadruple in min_trans:
		print(quadruple)
	print("")


	# test output_for_django(sj_list)
	print("")
	print("Django Output")
	print("Dijkstra")
	print(output_for_django(the_shortest_journey[1]))
	print("")
	print("Minimum Transfers")
	print(output_for_django(min_trans))
	print("")