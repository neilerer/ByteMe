# imports
import _0_0_data as data



def routes_at_stop(stop_dict, weekday, time_unit, stop):
	stop_data = stop_dict[weekday][time_unit][stop]
	route_list = list()
	for quadruple in stop_data:
		route = quadruple[3]
		if route not in route_list:
			route_list.append(route)
	return [stop, route_list]

def routes_dict(stop_dict):
	# make the framework
	r_dict = dict()
	for weekday in stop_dict:
		r_dict[weekday] = dict()
		for time_unit in stop_dict[weekday]:
			r_dict[weekday][time_unit] = dict()
	# populate the dictionary
	for weekday in stop_dict:
		for time_unit in stop_dict[weekday]:
			for stop in stop_dict[weekday][time_unit]:
				stop_and_routes_list = routes_at_stop(stop_dict, weekday, time_unit, stop)
				route_list = stop_and_routes_list[1]
				for route in route_list:
					if route not in r_dict[weekday][time_unit]:
						r_dict[weekday][time_unit][route] = set()
					for other_route in route_list:
						r_dict[weekday][time_unit][route].add(other_route)
	# return
	return r_dict


if __name__ == "__main__":
	stop_dict = data.get_pickle_file("stop_dict.p")
	r_dict = routes_dict(stop_dict)
	for weekday in r_dict:
		for time_unit in r_dict[weekday]:
			for route in r_dict[weekday][time_unit]:
				print(weekday, time_unit, route)
				print(r_dict[weekday][time_unit][route])
				print("")