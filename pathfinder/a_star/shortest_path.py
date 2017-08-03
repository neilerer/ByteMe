# imports
import os
import datetime
import os
import pickle
import time
import copy
import general
import merge_sort
import data_conversion_routes_to_stops as dcrts
import the_heuristic



def start_journey(start_stop_id, end_stop_id, stop_dict, been_list, journey_id_list):
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
	-- list[0] boolean indicating if we've found the shortest path
	-- list[1] a dictionary
	--- key journey_id
	--- value [total travel time, [(starting stop id, next stop id, travel time, route id)

	"""
	if start_stop_id == end_stop_id:
		return [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "n/a")]]}]
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



def continue_journey(journey_id_list, journies_dict, been_list, end_stop_id, stop_dict, target_routes):
	# sort journies so we know which is the shortest
	intermediate_dict = merge_sort.merge_sort_journies_dict(journies_dict)
	# sort journies so that a journey on the route gets precedence
	starting_dict = the_heuristic.target_route_goes_first(intermediate_dict, target_routes)
	# temp_dict that is the return object
	temp_dict = dict()
	# delete list
	delete_list = set()
	# iterate over items in starting_dict
	for jid in starting_dict:
		# details
		starting_details = starting_dict[jid]
		journey_time = starting_details[0]
		journey_details = starting_details[1]
		start_stop_id = journey_details[-1][0]
		next_stop_id = journey_details[-1][1]
		# skip if the next_stop has been visted before
		if next_stop_id in been_list:
			pass
		# if the next_stop is our destination, then we have our route
		elif next_stop_id == end_stop_id:
			temp_dict = dict()
			temp_dict[jid] = starting_details
			return [True, temp_dict]
		# otherwise, we create the next set of possible paths
		else:
			# we get the information about the next possible stop
			next_dict = stop_dict[next_stop_id]
			# iterate over possible next stops
			for stop_detail in next_dict:
				next_dict_stop_id = stop_detail[1]
				next_dict_time = stop_detail[2]
				# if the stop has not been visited
				if next_dict_stop_id not in been_list and (next_dict_stop_id != start_stop_id): #later condition prevents looping
					delete_list.add(jid) # we've extended this journey, so after temp_dict is full, delete this entry
					journey_id = journey_id_list[-1] + 1
					journey_id_list.append(journey_id)
					temp_details = copy.deepcopy(journey_details)
					temp_details.append(stop_detail)
					temp_dict[journey_id] = [round(journey_time + next_dict_time, 2), temp_details]
				# if the stop has been visited, we don't modify the journey
				else:
					temp_dict[jid] = starting_details
	# delete journeys we don't need to explore
	delete_list = list(delete_list)
	for jid in delete_list:
		try:
			del temp_dict[jid]
		except:
			pass
	# return
	return [False, temp_dict]



def find_shortest_path(start_stop_id, end_stop_id, stop_dict, target_routes):
	this_shortest_path = None
	this_found_shortest_path = False
	this_been_list = []
	this_journey_id_list = []
	this_journies_dict = dict()

	result = start_journey(start_stop_id, end_stop_id, stop_dict, this_been_list, this_journey_id_list)
	this_journies_dict = result[1]

	while this_found_shortest_path is False:
		result = continue_journey(this_journey_id_list, this_journies_dict, this_been_list, end_stop_id, stop_dict, target_routes)
		this_found_shortest_path = result[0]
		this_journies_dict = result[1]

	this_shortest_path = this_journies_dict

	return this_shortest_path
		
	

def shortest_path_test():
	stop_dict = dcrts.get_bus_stop_data()
	os.chdir("../")
	os.chdir("a_star")
	with open("a_star_shortest_path_test.txt", "w") as destination:
		for stop in stop_dict:
			# target_routes
			target_routes = the_heuristic.create_target_routes(stop, stop_dict)
			start_time = datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')
			destination.write("{} to all other stops started at {}".format(stop, start_time))
			destination.write("\n")
			destination.write("-------------------------------------------------------------------")
			destination.write("\n")
			big_time_start = time.time()
			for other_stop in stop_dict:
				small_time_start = time.time()
				sp = find_shortest_path(stop, other_stop, stop_dict, target_routes)
				destination.write("{} path to {} took {}".format(stop, other_stop, time.time() - small_time_start))
				destination.write("\n")
				destination.write(str(sp))
				destination.write("\n")
				destination.write("\n")
			destination.write("{} to all other stops took {}".format(stop, time.time() - big_time_start))
			destination.write("\n")
			destination.write("\n")
			destination.write("\n")
		destination.write("\n")
		destination.write("\n")
		destination.write("\n")
		destination.write("\n")


def testing_real_data():
	# get shit from file
	os.chdir("../")
	os.chdir("dijkstra")
	f = open("pathfinder_data.p", "rb")
	# load the pickle file
	pathfinder_dict = pickle.load(f)
	# close the pickle file
	f.close()
	os.chdir("../")
	os.chdir("a_star")

	monday = pathfinder_dict[0]
	nine_oclock = monday[9]

	target_routes = the_heuristic.create_target_routes(768, nine_oclock)

	sp = find_shortest_path(7158, 7571, nine_oclock, target_routes)

	return sp

if __name__ == "__main__":
	shortest_path_test()
	# print(testing_real_data())
