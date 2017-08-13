# imports
import _0_0_data as data
import _1_route_mapping as rm
import _2_route_planning as rp
import _3_route_connections as rc
import _4_shortest_paths as sp
import time
import datetime



# def key_partial_match(route, json_data):
# 	for jpi in json_data:
# 		if jpi[0:5] == route:
# 			return jpi

# def get_travel_time(json_data, first, second, route, weekday, time_unit):
# 	first_ctt = 0
# 	second_ctt = 0
# 	jpi = key_partial_match(route, json_data)
# 	# for jpi in json_data:
# 	# 	if jpi[0:5] == route:
# 	for key in json_data[jpi]:
# 		# [position, stop, weekday, time_unit]
# 		key_list = key.strip().split("-")
# 		# conditions
# 		if int(key_list[1]) == first and int(key_list[2]) == weekday and int(key_list[3]) == time_unit:
# 			first_ctt = float(json_data[jpi][key])
# 		elif int(key_list[1]) == first and int(key_list[2]) == weekday and int(key_list[3]) == time_unit:
# 			second_ctt = float(json_data[jpi][key])
# 		else:
# 			pass
# 	# models give garbage outputs; this is a temp fix until that is resolved
# 	return abs(abs(second_ctt) - abs(first_ctt))

def get_travel_time(ctt_dict, weekday, time_unit, route, first, second):
	first_ctt = 0
	second_ctt = 0
	for triple in ctt_dict[weekday][time_unit][route]:
		if triple[1] == first:
			first_ctt = triple[1]
		elif triple[1] == second:
			second_ctt = triple[1]
		else:
			pass
	# models have generated bogus data; this is a temp fix to keep values positive
	return abs(abs(second_ctt) - abs(first_ctt))

def path_id_add_ctt(path_id_dict, ctt_dict, weekday, time_unit):
	for route in path_id_dict:
		first = path_id_dict[route][0]
		second = path_id_dict[route][1]
		travel_time = get_travel_time(ctt_dict, weekday, time_unit, route, first, second)
		path_id_dict[route] = (first, second, travel_time)
	return path_id_dict

def ppt_dict_modification(pp_dict, ctt_dict, weekday, time_unit):
	for route_tuple in pp_dict:
		for path_id in pp_dict[route_tuple]:
			path_id_dict = path_id_add_ctt(pp_dict[route_tuple][path_id], ctt_dict, weekday, time_unit)
			pp_dict[route_tuple][path_id] = path_id_dict

def pathfinder(pp_dict):
	pathfinder_dict = dict()
	for route_tuple in pp_dict:
		for path_id in pp_dict[route_tuple]:
			suggested_path = pp_dict[route_tuple][path_id]
			time = 0
			for route in suggested_path:
				time += suggested_path[route][2]
			pathfinder_dict[time] = suggested_path
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

	# log file
	log_file = open("_6_log_file.txt", "a")

	weekday = 0
	time_unit = 10
	start = 400
	end = 807

	# log entry
	coder = "ojh"
	log_entry = "reduction of operations in pathfinder get_travel_time"
	log_file.write(
		"{}\n\n".format(datetime.datetime.now())
		+
		"Comments\n"
		+
		log_entry +"\n\n"
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

	grc_start = time.time()
	grc_dict = rc.get_route_connections(stop_dict, ctt_dict, r_dict, weekday, time_unit, start, end)
	grc_time = time.time() - grc_start
	log_file.write("grc_dict took {} to generate\n".format(grc_time))

	pp_dict_start = time.time()
	pp_dict = sp.possible_paths_dictionary(grc_dict, start, end)
	pp_dict_time = time.time() - pp_dict_start
	log_file.write("pp_dict took {} to generate\n".format(pp_dict_time))

	pp_dict_modification_start = time.time()
	ppt_dict_modification(pp_dict, ctt_dict, weekday, time_unit)
	pp_dict_modification_time = time.time() - pp_dict_modification_start
	log_file.write("pp_dict_modification took {} to generate\n\n".format(pp_dict_modification_time))

	# for route_tuple in pp_dict:
	# 	print(route_tuple)
	# 	print(pp_dict[route_tuple])
	# 	print("")

	pathfinder_dict = pathfinder(pp_dict)
	log_file.write("Output\n")
	for time in pathfinder_dict:
		log_file.write("{} : {}\n".format(time, pathfinder_dict[time]))
	log_file.write("\n\n\n\n")


