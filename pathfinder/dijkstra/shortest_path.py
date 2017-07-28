# imports
import general
import merge_sort
import data_conversion_routes_to_stops as dcrts



def start_journey(start_stop_id, stop_dict, been_list, journey_id_list, journies_dict):
	# instantiate journey_id
	journey_id = 0
	# record that we've been to this bus stop
	been_list.append(start_stop_id)
	# find the data we will use to start our journies
	list_of_next_stop_details = stop_dict[start_stop_id]
	# populate journies_dict
	for stop_detail in list_of_next_stop_details:
		next_stop_id = stop_detail[1]
		next_time = stop_detail[2]
		# check if we've already been there
		if next_stop_id not in been_list:
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			journies_dict[journey_id] = [next_time, [stop_detail]]
			# increment the journey_id
			journey_id += 1



def continue_journey(end_stop_id, stop_dict, been_list, journey_id_list, journies_dict, shortest_path, found_shortest_path):
	# instatiate journey_id
	journey_id = journey_id_list[-1] + 1
	# sort journies so we know which is the shortest
	starting_dict = merge_sort.merge_sort_journies_dict(journies_dict)
	# get the starting details
	starting_details = starting_dict.pop(next(iter(starting_dict)))
	journey_time = starting_details[0]
	journey_details = starting_details[1]
	start_stop_id = journey_details[-1][0]
	next_stop_id = journey_details[-1][1]
	# delete the journey that does should not be there any longer
	starting_key = next(iter(starting_dict))
	del journies_dict[starting_key]
	# # check if we are at the destination
	if start_stop_id == end_stop_id:
		found_shortest_path = True
		shortest_path = starting_details
	elif next_stop_id in been_list:
		pass
	else:
		been_list.append(next_stop_id)
		list_of_next_stop_details = stop_dict[next_stop_id]
		# populate journies_dict
		for stop_detail in list_of_next_stop_details:
			current_stop_id = stop_detail[1]
			next_time = stop_detail[2]
			# check if we've already been there
			if current_stop_id not in been_list:
				# record the journey_id
				journey_id_list.append(journey_id)
				# create the journey details
				journey_details.append(stop_detail)
				journies_dict[journey_id] = [round(journey_time + next_time, 2), journey_details]
				# increment the journey_id
				journey_id = journey_id_list[-1] + 1



if __name__ == "__main__":
	# data objects
	stop_dict = dcrts.get_bus_stop_data()
	been_list = []
	journey_id = 0
	journey_id_list = []
	journies_dict = dict()
	shortest_path = None
	found_shortest_path = False

	for stop in stop_dict:
		print(stop)
		print(stop_dict[stop])
		print("")

	start_journey(78, stop_dict, been_list, journey_id_list, journies_dict)
	print("starting journey dict")
	print(journies_dict)
	print("")

	continue_journey(79, stop_dict, been_list, journey_id_list, journies_dict, shortest_path, found_shortest_path)
	print("journeys at depth 1")
	print(journies_dict)
	print("")