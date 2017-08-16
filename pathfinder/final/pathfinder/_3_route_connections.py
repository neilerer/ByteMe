# imports
import _0_0_data as data
import _1_route_mapping as rm
import _2_route_planning as rp
from operator import itemgetter
import time


def stop_routes(stop_quadruples_list):
	stop_routes_list = list()
	for quadruple in stop_quadruples_list:
		stop_routes_list.append(quadruple[3])
	return stop_routes_list

def get_possible_routes(stop_dict, r_dict, weekday, time_unit, start_stop, end_stop):
	# inputs
	possible_pairs = [(start, end) for start in stop_routes(stop_dict[weekday][time_unit][start_stop]) for end in stop_routes(stop_dict[weekday][time_unit][end_stop])]
	# generation
	possible_routes = [rp.minimum_transfers(r_dict, weekday, time_unit, start_route, end_route) for (start_route, end_route) in possible_pairs]
	# sorting
	possible_routes.sort(key=len)
	return possible_routes

def route_connections(route_list, ctt_dict, weekday, time_unit, end):
	route_connections_dict = dict()
	if len(route_list) < 1:
		return None
	elif len(route_list) == 1:
		# first_route = route_list[0]
		for f_tuple in ctt_dict[weekday][time_unit][route_list[0]]:
			#key = (route_list[0], route_list[0])
			#value = f_tuple[1]
			if (route_list[0], route_list[0]) not in route_connections_dict:
				route_connections_dict[(route_list[0], route_list[0])] = [f_tuple[1]]
			else:
				route_connections_dict[(route_list[0], route_list[0])].append(f_tuple[1])
			# don't need to check past the destination
			if f_tuple[1] == end:
				return route_connections_dict
	else:
		for i in range(1, len(route_list), 1):
			# first_route = route_list[i - 1]
			# second_route = route_list[i]
			for f_tuple in ctt_dict[weekday][time_unit][route_list[i - 1]]:
				for s_tuple in ctt_dict[weekday][time_unit][route_list[i]]:
					# f_stop = f_tuple[1]
					# s_stop = s_tuple[1]
					if f_tuple[1] == s_tuple[1]:
						# key = (route_list[i - 1], route_list[i])
						# connecting stop
						# value = f_tuple[1]
						if (route_list[i - 1], route_list[i]) not in route_connections_dict:
							route_connections_dict[(route_list[i - 1], route_list[i])] = [f_tuple[1]]
						else:
							route_connections_dict[(route_list[i - 1], route_list[i])].append(f_tuple[1])
						# don't need to check past the destination
						if f_tuple[1] == end:
							return route_connections_dict
	return route_connections_dict

def get_route_connections(stop_dict, ctt_dict, r_dict, weekday, time_unit, start, end):
	grc_dict = dict()
	pr_dict = get_possible_routes(stop_dict, r_dict, weekday, time_unit, start, end)
	for i in range(0, len(pr_dict), 1):
		route_list = pr_dict[i]
		# grd_dict = get_route_data(route_list, json_data, weekday, time_unit)
		grc_dict[tuple(route_list)] = route_connections(route_list, ctt_dict, weekday, time_unit, end)
	# THIS SEGMENT ONLY EXISTS SO THAT THIS CODE CAN RUN QUICKLY ON VERY LIGHTWEIGHT MACHINES, ALTHOUGH PRAGMATICALLY IS MAKES NO DIFFERENCE AS WE HAVE NO SIGHT OF WHICH STOPS ARE BEST FOR TRANSFERING
	# reducing output so can run well on lightweight machines; otherwise would keep for robustness
	for route_tuple in grc_dict:
		for route_pair in grc_dict[route_tuple]:
			grc_dict[route_tuple][route_pair] = [grc_dict[route_tuple][route_pair][-1]]
	# return
	return grc_dict




if __name__ == "__main__":
	# data
	print("Loading stop_dict . . .")
	stop_dict = data.get_pickle_file("stop_dict.p")
	print("Generating route dict . . .")
	r_dict = rm.routes_dict(stop_dict)
	print("Loading ctt_dict . . .")
	ctt_dict = data.get_pickle_file("ctt_dict.p")

	weekday = 0
	time_unit = 10
	start = 2065
	end = 768

	grc_dict = get_route_connections(stop_dict, ctt_dict, r_dict, weekday, time_unit, start, end)
	for item in grc_dict:
		print(item)
		print(grc_dict[item])
		print("")