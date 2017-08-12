# imports
import data
import dijkstra_merge_sort
import _1_route_mapping as rm
import _2_route_planning as rp
import _3_route_connections as rc
import itertools
import _4_shortest_paths as sp



def get_travel_time(json_data, first, second, route, weekday, time_unit):
	first_ctt = 0
	second_ctt = 0
	for jpi in json_data:
		if jpi[0:5] == route:
			for key in json_data[jpi]:
				key_list = key.strip().split("-")
				position = int(key_list[0])
				stop = int(key_list[1])
				wd = int(key_list[2])
				tu = int(key_list[3])
				ctt = float(json_data[jpi][key])
				key_list.append(ctt)
				# 
				if stop == first and wd == weekday and tu == time_unit:
					first_ctt = ctt
				if stop == second and wd == weekday and tu == time_unit:
					second_ctt = ctt
	# models give garbage outputs; this is a temp fix until that is resolved
	return abs(abs(second_ctt) - abs(first_ctt))

def path_id_add_ctt(path_id_dict, json_data, weekday, time_unit):
	for route in path_id_dict:
		first = path_id_dict[route][0]
		second = path_id_dict[route][1]
		travel_time = get_travel_time(json_data, first, second, route, weekday, time_unit)
		path_id_dict[route] = (first, second, travel_time)
	return path_id_dict

def ppt_dict_modification(pp_dict, json_data, weekday, time_unit):
	for route_tuple in pp_dict:
		for path_id in pp_dict[route_tuple]:
			path_id_dict = path_id_add_ctt(pp_dict[route_tuple][path_id], json_data, weekday, time_unit)
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
	print("Loading model dict . . .")
	model_dict = data.get_model_data()
	print("Loading route dict . . .")
	r_dict = rm.routes_dict(model_dict)
	print("Loading JSON data . . .")
	json_data = data.get_actual_model_data()

	weekday = 0
	time_unit = 10
	start = 40
	end = 4486

	grc_dict = rc.get_route_connections(model_dict, json_data, r_dict, weekday, time_unit, start, end)

	pp_dict = sp.possible_paths_dictionary(grc_dict, start, end)
	# for route_tuple in pp_dict:
	# 	print(route_tuple)
	# 	print(pp_dict[route_tuple])
	# 	print("")

	# print(get_travel_time(json_data, 40, 6230, '00090', weekday, time_unit))
	# print(get_travel_time(json_data, 6230, 336, '00830', weekday, time_unit))

	ppt_dict_modification(pp_dict, json_data, weekday, time_unit)
	# for route_tuple in pp_dict:
	# 	print(route_tuple)
	# 	print(pp_dict[route_tuple])
	# 	print("")

	pathfinder_dict = pathfinder(pp_dict)
	for time in pathfinder_dict:
		print(time)
		print(pathfinder_dict[time])


