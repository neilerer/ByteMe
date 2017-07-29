# imports
import copy
import general
import merge_sort
import data_conversion_routes_to_stops as dcrts



def start_journey(start_stop_id, stop_dict, been_list, journey_id_list):
	"""
	Purpose
	- to generate the starting options for a journey on the bus system


	Input
	- start_stop_id
	-- int representation of the bus stop id
	
	- stop_dict
	-- output of dcrts.get_bus_stop_data()
	--- dictionary
	---- key is stop id
	---- value is a list containing every triple of (stop_id, next_stop_id, journey_time)

	- been_list
	-- a list containing all stops that have been visited

	- journey_id_list
	-- a list containing the journey ids of each journey we've explored


	Output
	- list
	-- list[0] boolean indicating if we've found the shortest path (in this function it will always be False)
	-- list[1] a dictionary
	--- key journey_id
	--- value [total travel time, [(starting stop id, next stop id, travel time, route id)

	"""
	# temp_dict
	temp_dict = dict()
	# instantiate journey_id
	try:
		journey_id = journey_id_list[-1] + 1
	except:
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
			temp_dict[journey_id] = [next_time, [stop_detail]]
			# increment the journey_id
			journey_id += 1
	return [False, temp_dict]



def continue_journey(journey_id_list, journies_dict, been_list, end_stop_id, stop_dict):
	# sort journies so we know which is the shortest
	starting_dict = merge_sort.merge_sort_journies_dict(journies_dict)
	# temp_dict
	temp_dict = dict()
	# iterate over items in starting_dict
	for jid in starting_dict:
		starting_details = starting_dict[jid]
		journey_time = starting_details[0]
		journey_details = starting_details[1]
		start_stop_id = journey_details[-1][0]
		next_stop_id = journey_details[-1][1]
		# 
		if next_stop_id in been_list:
			pass
		elif next_stop_id == end_stop_id:
			temp_dict = dict()
			temp_dict[jid] = starting_details
			return [True, temp_dict]
		else:
			next_dict = stop_dict[next_stop_id]
			for stop_detail in next_dict:
				next_dict_stop_id = stop_detail[1]
				next_dict_time = stop_detail[2]
				if next_dict_stop_id not in been_list:
					journey_id = journey_id_list[-1] + 1
					journey_id_list.append(journey_id)
					temp_details = copy.deepcopy(journey_details)
					temp_details.append(stop_detail)
					temp_dict[journey_id] = [round(journey_time + next_dict_time, 2), temp_details]
				else:
					temp_dict[jid] = starting_details
	return [False, temp_dict]



def find_shortest_path(start_stop_id, end_stop_id, stop_dict):
	this_shortest_path = None
	this_found_shortest_path = False
	this_been_list = []
	this_journey_id_list = []
	this_journies_dict = dict()

	result = start_journey(start_stop_id, stop_dict, this_been_list, this_journey_id_list)
	this_journies_dict = result[1]

	while this_found_shortest_path is False:
		result = continue_journey(this_journey_id_list, this_journies_dict, this_been_list, end_stop_id, stop_dict)
		this_found_shortest_path = result[0]
		this_journies_dict = result[1]

	this_shortest_path = this_journies_dict

	return this_shortest_path
		
	

if __name__ == "__main__":
	# data objects
	stop_dict = dcrts.get_bus_stop_data()
	# print(find_shortest_path(72, 82, stop_dict))
	print(find_shortest_path(32, 73, stop_dict))
	print(find_shortest_path(72, 20, stop_dict))








	# been_list = []
	# journey_id = 0
	# journey_id_list = []
	# journies_dict = dict()
	
	# shortest_path = None
	# found_shortest_path = False

	# for stop in stop_dict:
	# 	print(stop)
	# 	print(stop_dict[stop])
	# 	print("")

	# start_journey(78, stop_dict, been_list, journey_id_list, journies_dict)
	# print("starting journey dict")
	# print(journies_dict)
	# print("")

	# continue_journey(79, stop_dict, been_list, journey_id_list, journies_dict, shortest_path, found_shortest_path)
	# print("journeys at depth 1")
	# print(journies_dict)
	# print("")

	# print(shortest_path)



# def continue_journey(end_stop_id, stop_dict, been_list, journey_id_list, journies_dict, shortest_path, found_shortest_path):
# 	# instatiate journey_id
# 	journey_id = journey_id_list[-1] + 1
# 	# sort journies so we know which is the shortest
# 	starting_dict = merge_sort.merge_sort_journies_dict(journies_dict)
# 	# get the starting details
# 	starting_dict_length = len(starting_dict)
# 	for i in range(0, starting_dict_length, 1):
# 		starting_key = next(iter(starting_dict))
# 		starting_details = starting_dict.pop(next(iter(starting_dict)))
# 		journey_time = starting_details[0]
# 		journey_details = starting_details[1]
# 		start_stop_id = journey_details[-1][0]
# 		next_stop_id = journey_details[-1][1]
# 		# # delete the journey that does should not be there any longer
# 		# del journies_dict[starting_key]
# 		# check if we are at the destination
# 		if next_stop_id == end_stop_id:
# 			shortest_path = starting_details
# 			found_shortest_path = True
# 		# elif next_stop_id in been_list:
# 			# pass
# 		else:
# 			been_list.append(next_stop_id)
# 			list_of_next_stop_details = stop_dict[next_stop_id]
# 			# populate journies_dict
# 			for stop_detail in list_of_next_stop_details:
# 				current_stop_id = stop_detail[1]
# 				next_time = stop_detail[2]
# 				# check if we've already been there
# 				if current_stop_id not in been_list:
# 					# record the journey_id
# 					journey_id_list.append(journey_id)
# 					# create the journey details
# 					journey_details.append(stop_detail)
# 					journies_dict[journey_id] = [round(journey_time + next_time, 2), journey_details]
# 					# increment the journey_id
# 					journey_id = journey_id_list[-1] + 1



# def continue_journey(end_stop_id, stop_dict, been_list, journey_id_list, journies_dict, shortest_path, found_shortest_path):
# 	# instatiate journey_id
# 	journey_id = journey_id_list[-1] + 1
# 	# sort journies so we know which is the shortest
# 	starting_dict = merge_sort.merge_sort_journies_dict(journies_dict)
# 	temp_dict = dict()
# 	# 
# 	for jid in starting_dict:
# 		starting_details = starting_dict[jid]
# 		journey_time = starting_details[0]
# 		journey_details = starting_details[1]
# 		start_stop_id = journey_details[-1][0]
# 		next_stop_id = journey_details[-1][1]
# 		# 
# 		if next_stop_id == end_stop_id:
# 			shortest_path = starting_details
# 			found_shortest_path = True
# 			temp_dict = {}
# 			temp_dict[journey_id] = [round(journey_time + next_time, 2), journey_details]
# 			return [temp_dict, True]
# 		#
# 		elif next_stop_id in been_list:
# 			pass
# 		#
# 		else:
# 			been_list.append(next_stop_id)
# 			list_of_next_stop_details = stop_dict[next_stop_id]
# 			# 
# 			for stop_detail in list_of_next_stop_details:
# 				current_stop_id = stop_detail[1]
# 				next_time = stop_detail[2]
# 				# check if we've already been there
# 				if current_stop_id not in been_list:
# 					# record the journey_id
# 					journey_id_list.append(journey_id)
# 					# create the journey details
# 					journey_details.append(stop_detail)
# 					# create an entry
# 					temp_dict[journey_id] = [round(journey_time + next_time, 2), journey_details]
# 					# increment the journey_id
# 					journey_id = journey_id_list[-1] + 1
# 	return [temp_dict, False]