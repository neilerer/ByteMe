# imports
import _0_0_data as data
import _1_route_mapping as rm
import _2_route_planning as rp
import _3_route_connections as rc
import _4_shortest_paths as sp
import time
import datetime
from operator import itemgetter



def get_travel_time(ctt_dict, weekday, time_unit, route, first, second):
	first_ctt = 0
	second_ctt = 0
	# if ctt_dict were a dictionary, this would be much faster; might change if I have time
	for triple in ctt_dict[weekday][time_unit][route]:
		if triple[1] == first:
			first_ctt = triple[2]
		elif triple[1] == second:
			second_ctt = triple[2]
		else:
			pass
	# models have generated bogus data; this is a temp fix to keep values positive
	return abs(abs(second_ctt) - abs(first_ctt))



def pathfinder(clean_pp_dict, ctt_dict, weekday, time_unit):
	pathfinder_dict = dict()
	for route_tuple in clean_pp_dict:
		pathfinder_list = [0.00, dict()]
		path = clean_pp_dict[route_tuple]
		route_count = 0
		for route in path:
			start = path[route][0]
			end = path[route][1]
			travel_time = get_travel_time(ctt_dict, weekday, time_unit, route, start, end)
			pathfinder_list[0] += travel_time + (route_count * 300)
			pathfinder_list[1][route] = (start, end, travel_time + (route_count * 300))
			route_count = 1
		pathfinder_dict[pathfinder_list[0]] = pathfinder_list[1]
	# sort pathfinder_dict
	key_list = list()
	for key in pathfinder_dict:
		key_list.append(key)
	key_list.sort()
	final_dict = dict()
	for key in key_list:
		final_dict[key] = pathfinder_dict[key]
	return final_dict



if __name__ == "__main__":
	# data
	print("Loading stop_dict . . .")
	stop_dict = data.get_pickle_file("stop_dict.p")
	print("Generating route dict . . .")
	r_dict = rm.routes_dict(stop_dict)
	print("Loading ctt_dict . . .")
	ctt_dict = data.get_pickle_file("ctt_dict.p")

	# inputs
	weekday = 0
	time_unit = 10
	start = 3058
	end = 7174

	# generated data
	grc_start = time.time()
	grc_dict = rc.get_route_connections(stop_dict, ctt_dict, r_dict, weekday, time_unit, start, end)
	grc_time = time.time() - grc_start

	pp_dict_start = time.time()
	pp_dict = sp.possible_paths_dictionary(grc_dict, start, end)
	pp_dict_time = time.time() - pp_dict_start

	clean_pp_dict_start = time.time()
	clean_pp_dict = sp.clean_possible_paths_dicitonary(pp_dict)
	clean_pp_dict_time = time.time() - clean_pp_dict_start

	pathfinder_dict_start = time.time()
	pathfinder_dict = pathfinder(clean_pp_dict, ctt_dict, weekday, time_unit)
	pathfinder_dict_time = time.time() - pathfinder_dict_start



	# log file
	log_file = open("_6_log_file.txt", "a")

	user = "ojh"
	
	log_entry = "Testing"
	
	log_file.write(
		"{}\n\n".format(datetime.datetime.now())
		+
		"Comments\n"
		+
		log_entry + "\n\n"
		+
		"User\n"
		+
		user + "\n\n"
		+
		"Inputs\n"
		+
		"weekday = {}\n".format(weekday)
		+
		"time_unit = {}\n".format(time_unit)
		+
		"start = {}\n".format(start)
		+
		"end = {}\n\n".format(end)
		+
		"Performance\n")

	log_file.write("grc_dict took {} to generate\n".format(grc_time))


	log_file.write("pp_dict took {} to generate\n".format(pp_dict_time))


	log_file.write("clean_pp_dict took {} to generate\n".format(clean_pp_dict_time))


	log_file.write("pathfinder_dict took {} to generate\n".format(pathfinder_dict_time))

	log_file.write("entire process took {}\n\n".format(grc_time + pp_dict_time + clean_pp_dict_time + pathfinder_dict_time))
	
	log_file.write("Output\n")
	for item in pathfinder_dict:
		log_file.write("{}: {}\n".format(item, pathfinder_dict[item]))
	log_file.write("\n\n\n\n")



