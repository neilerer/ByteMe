# imports
import data
import dijkstra_merge_sort
import _1_route_mapping as rm
import _2_route_planning as rp
import _3_route_connections as rc
import itertools
import _4_shortest_paths as sp



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
	for route_tuple in pp_dict:
		print(route_tuple)
		print(pp_dict[route_tuple])
		print("")