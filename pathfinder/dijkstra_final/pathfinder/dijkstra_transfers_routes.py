# imports
import copy
import data
import merge_sort



def time_unit_model_dict(weekday, time_unit, model_dict):
	# time_unit_dict
	return model_dict[weekday][time_unit]



def start_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set):
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	if start_stop_id == end_stop_id:
		return [True, {0 :[[0, {}, 0, {}], [(start_stop_id, end_stop_id, 0.00, None) ] ] } ]
	# been_set
	been_set.add(start_stop_id)
	# ending_dict
	ending_dict = journies_dict
	# find the quadruples associated with potential next stops
	list_of_start_stop_quadruples = time_unit_dict[start_stop_id]
	# populate ending_dict
	for quadruple in list_of_start_stop_quadruples:
		# extract information
		current_stop_id = quadruple[0]
		next_stop_id = quadruple[1]
		next_stop_journey_time = quadruple[2]
		next_stop_route = quadruple[3]
		# determine if a journey should be created
		if (next_stop_id is not None):
			# create the journey_id
			try:
				jouney_id = journey_id_list[-1] + 1
			except:
				journey_id = 0
			# record the journey_id
			journey_id_list.append(journey_id)
			# increment journey_id
			journey_id += 1
			# create the journey details
			ending_dict[journey_id] = [ [0, [next_stop_route], next_stop_journey_time, [start_stop_id]], [quadruple] ]
	# return
	return [False, ending_dict]



def continue_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set):
	# time_unit_dict
	time_unit_dict = time_unit_model_dict(weekday, time_unit, model_dict)
	# instantiate continuing_dict
	continuing_dict = journies_dict
	# sort continuing_dict so that the shortest journey is considered
	continuing_dict = merge_sort.merge_sort(continuing_dict)
	# pop the shortest journey
	current_shortest_journey = merge_sort.get_first_entry_of_dict(continuing_dict)
	# unpack the shortest journey
	current_journey_contents = current_shortest_journey[1]
	current_journey_id = current_shortest_journey[0]
	current_transfers = current_journey_contents[0][0]
	current_visited_routes = current_journey_contents[0][1]
	current_journey_time = current_journey_contents[0][2]
	current_visited_stops = current_journey_contents[0][3]
	current_journey_path = current_journey_contents[1]
	current_stop_details = current_journey_path[-1]
	current_stop = current_stop_details[0]
	next_stop = current_stop_details[1]
	next_stop_time = current_stop_details[2]
	next_stop_route = current_stop_details[3]
	# contine the shortest journey
	if next_stop == end_stop_id:
		return [True, {current_journey_id : current_journey_contents}]
	elif next_stop in been_set:
		del continuing_dict[current_journey_id]
		return [False, continuing_dict]
	else:
		# update been_set
		been_set.add(next_stop)
		print(been_set)
		# iterate over the quadruples at the next stop
		for quadruple in time_unit_dict[next_stop]:
			# extract information
			destination_stop = quadruple[1]
			destination_time = quadruple[2]
			destination_route = quadruple[3]
			# skip if we've already been on that route but are not currently on it
			if (destination_route in current_visited_routes) and (destination_route != next_stop_route):
				print("been on route")
				pass
			# skip if we've already been to this stop
			elif destination_stop in current_visited_stops:
				print("been to that stop")
				pass
			# skip if the destination stop is None
			elif destination_stop is None:
				print("end of the line")
				pass
			# determine if a journey should be created
			else:
				# generate new data
				continuing_journey_id = journey_id_list[-1]
				continuing_journey_id += 1
				continuing_journey_contents = copy.deepcopy(current_shortest_journey[1])
				continuing_transfers = continuing_journey_contents[0][0]
				continuing_visited_routes = continuing_journey_contents[0][1]
				continuing_journey_time = continuing_journey_contents[0][2]
				continuing_visited_stops = continuing_journey_contents[0][3]
				continuing_journey_path = continuing_journey_contents[1]
				continuing_stop_details = continuing_journey_path[-1]
				continuing_stop = continuing_stop_details[0]
				# record that we've been to next_stop (we're iterating over its possibilities now)
				continuing_visited_stops.append(next_stop)
				# record the route we took from next to destination
				if destination_route not in continuing_visited_routes:
					continuing_visited_routes.append(destination_route)
				# extend the continuing_journey_path
				if next_stop_route == destination_route:
					continuing_journey_contents[0][2] += destination_time
					continuing_journey_path.append(quadruple)
					continuing_dict[continuing_journey_id] = continuing_journey_contents
					journey_id_list.append(continuing_journey_id)
				else:
					continuing_journey_contents[0][0] += 1
					continuing_journey_contents[0][2] += destination_time
					continuing_journey_path.append((next_stop, destination_stop, destination_time + 300, destination_route))
					continuing_dict[continuing_journey_id] = continuing_journey_contents
					journey_id_list.append(continuing_journey_id)
		# this journey_id lead to nowhere
		# del continuing_dict[current_journey_id]
		# return
		return [False, continuing_dict]




def dijkstra(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set):
	# data objects
	found_shortest_path = False
	# start
	result = start_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
	found_shortest_path = result[0]
	journies_dict = result[1]

	#test
	print("")
	print("Round 1")
	for item in journies_dict:
		print(item)
		print(journies_dict[item])
	print("")

	for i in range(0, 2, 1):
		print("")
		print("Round {}".format(i))
		result = continue_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
		found_shortest_path = result[0]
		journies_dict = result[1]
		for item in journies_dict:
			print(item)
			print(journies_dict[item])
		print("")

	#continue
	while found_shortest_path is False:
		result = continue_shortest_path(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
		found_shortest_path = result[0]
		journies_dict = result[1]
	#return
	shortest_path_details = None
	for journey_id in journies_dict:
		shortest_path_details = journies_dict[journey_id]
	return shortest_path_details



def pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict):
	journey_id_list = list()
	journies_dict = dict()
	been_set = set()
	the_shortest_journey = dijkstra(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
	return the_shortest_journey



if __name__ == "__main__":
	# data
	print("Loading the model data . . .")
	model_dict = data.get_model_data()

	# inputs
	start_stop_id =  768
	end_stop_id = 774#1509
	weekday = 0
	time_unit = 10

	# test pathfinder
	print("")
	print("Dijkstra Minimum Transfers")
	the_shortest_journey = pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict)
	print("Tranfers: {}".format(the_shortest_journey[0]))
	print("Path")
	for quadruple in the_shortest_journey[1]:
		print(quadruple)
	print("")