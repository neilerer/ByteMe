# imports
import data_1_linked_list as d1
import data_2_possible_paths as d2
import pathfinder_1_possible_paths as p1
import shortest_path as sp



# source data
stop_dict = d1.linked_list_for_export()
possible_paths_dict = d2.possible_paths()
all_stops_list = [stop for stop in stop_dict]



def get_possible_paths():
	for start in all_stops_list:
		for end in all_stops_list:
			print(start)
			print(end)
			print(sp.get_possible_paths(start, end, stop_dict, possible_paths_dict))
			print("")

get_possible_paths()