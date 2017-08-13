# imports
import _0_0_data as data
import _1_route_mapping as rm
import _2_route_planning as rp
import _3_route_connections as rc
import itertools



def possible_paths_individual(grc_dict, route_tuple, start, end):
	possible_paths_list = [[start]]
	for connection in grc_dict[route_tuple]:
		possible_paths_list.append(grc_dict[route_tuple][connection])
	possible_paths_list.append([end])
	return possible_paths_list

def possible_paths_entire(grc_dict, start, end):
	possible_paths_dict = dict()
	for route_tuple in grc_dict:
		possible_paths_dict[route_tuple] = possible_paths_individual(grc_dict, route_tuple, start, end)
	return possible_paths_dict

def possible_paths(grc_dict, start, end):
	the_possible_paths = dict()
	possible_paths_dict = possible_paths_entire(grc_dict, start, end)
	for route_tuple in possible_paths_dict:
		stop_list = possible_paths_dict[route_tuple]
		the_possible_paths[route_tuple] = list()
		for sub_list in itertools.product(*stop_list):
			the_possible_paths[route_tuple].append(sub_list)
	return the_possible_paths

def possible_paths_dictionary(grc_dict, start, end):
	the_possible_paths = possible_paths(grc_dict, start, end)
	pp_dict = dict()
	for route_tuple in the_possible_paths:
		pp_dict[route_tuple] = dict()
		route_tuple_dict = pp_dict[route_tuple]
		path_list = the_possible_paths[route_tuple]
		path_id = 0
		for path in path_list:
			pair_list = list()
			for i in range(1, len(path)):
				pair_list.append((path[i -1], path[i]))
			route_tuple_dict[path_id] = dict()
			path_id_dict = route_tuple_dict[path_id]
			for i in range(0, len(pair_list)):
				path_id_dict[route_tuple[i]] = pair_list[i]
			path_id += 1
	return pp_dict



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
	start = 400
	end = 807

	grc_dict = rc.get_route_connections(model_dict, json_data, r_dict, weekday, time_unit, start, end)
	for item in grc_dict:
		print(item)
		print(grc_dict[item])
		print("")

	possible_paths_dict = possible_paths_entire(grc_dict, start, end)
	for item in possible_paths_dict:
		print(item)
		print(possible_paths_dict[item])
		print("")

	the_possible_paths = possible_paths(grc_dict, start, end)
	for route_tuple in the_possible_paths:
		print(route_tuple)
		print(the_possible_paths[route_tuple])
		print("")

	pp_dict = possible_paths_dictionary(grc_dict, start, end)
	for route_tuple in pp_dict:
		print(route_tuple)
		print(pp_dict[route_tuple])
		print("")