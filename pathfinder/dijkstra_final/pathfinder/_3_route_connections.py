# imports
import _0_0_data as data
import _1_route_mapping as rm
import _2_route_planning as rp
from operator import itemgetter


def stop_routes(stop_quadruples_list):
	stop_routes_list = list()
	for quadruple in stop_quadruples_list:
		stop_routes_list.append(quadruple[3])
	return stop_routes_list

def get_possible_routes(model_dict, r_dict, weekday, time_unit, start_stop, end_stop):
	# data
	start_routes = stop_routes(model_dict[weekday][time_unit][start_stop])
	end_routes = stop_routes(model_dict[weekday][time_unit][end_stop])
	# inputs
	possible_pairs = [(start, end) for start in start_routes for end in end_routes]
	# generation
	possible_routes = [rp.minimum_transfers(r_dict, weekday, time_unit, start_route, end_route) for (start_route, end_route) in possible_pairs]
	# sorting
	possible_routes.sort(key=len)
	return possible_routes

def get_route_data(route_list, json_data, weekday, time_unit):
	grd_dict = dict()
	for route in route_list:
		grd_dict[route] = list()
	for route in route_list:
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
					if wd == weekday and tu == time_unit:
						grd_dict[jpi[0:5]].append((position, stop, ctt))
	for route in grd_dict:
		grd_dict[route].sort(key=itemgetter(0))
	# return
	return grd_dict

def route_connections(route_list, grd_dict):
	route_connections_dict = dict()
	if len(route_list) < 1:
		return None
	elif len(route_list) == 1:
		first_route = route_list[0]
		for f_tuple in grd_dict[first_route]:
			key = (first_route, first_route)
			value = f_tuple[1]
			if key not in route_connections_dict:
				route_connections_dict[key] = [value]
			else:
				route_connections_dict[key].append(value)
	else:
		for i in range(1, len(route_list), 1):
			first_route = route_list[i - 1]
			second_route = route_list[i]
			for f_tuple in grd_dict[first_route]:
				for s_tuple in grd_dict[second_route]:
					f_stop = f_tuple[1]
					s_stop = s_tuple[1]
					if f_stop == s_stop:
						key = (first_route, second_route)
						# connecting stop
						value = f_tuple[1]
						if key not in route_connections_dict:
							route_connections_dict[key] = [value]
						else:
							route_connections_dict[key].append(value)
	return route_connections_dict

def get_route_connections(model_dict, json_data, r_dict, weekday, time_unit, start, end):
	grc_dict = dict()
	pr_dict = get_possible_routes(model_dict, r_dict, weekday, time_unit, start, end)
	for i in range(0, len(pr_dict), 1):
		route_list = pr_dict[i]
		grd_dict = get_route_data(route_list, json_data, weekday, time_unit)
		grc_dict[tuple(route_list)] = route_connections(route_list, grd_dict)
	# THIS SEGMENT ONLY EXISTS SO THAT THIS CODE CAN RUN QUICKLY ON VERY LIGHTWEIGHT MACHINES, ALTHOUGH PRAGMATICALLY IS MAKES NO DIFFERENCE AS WE HAVE NO SIGHT OF WHICH STOPS ARE BEST FOR TRANSFERING
	# reducing output so can run well on lightweight machines; otherwise would keep for robustness
	for route_tuple in grc_dict:
		for route_pair in grc_dict[route_tuple]:
			grc_dict[route_tuple][route_pair] = [grc_dict[route_tuple][route_pair][-1]]
	# return
	return grc_dict




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

	grc_dict = get_route_connections(model_dict, json_data, r_dict, weekday, time_unit, start, end)
	for item in grc_dict:
		print(item)
		print(grc_dict[item])
		print("")