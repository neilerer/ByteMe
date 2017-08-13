# imports
import _0_0_data as data



# source data
def weekday_list(model_dict):
	wd_list = list()
	for weekday in model_dict:
		wd_list.append(weekday)
	return wd_list

def time_unit_list(wd_list):
	model_dict = data.get_model_data()
	tu_list = set()
	for weekday in wd_list:
		for time_unit in model_dict[weekday]:
			tu_list.add(time_unit)
	return list(tu_list)

def stop_id_dict(model_dict):
	stop_id_dict = dict()
	for weekday in model_dict:
		stop_id_dict[weekday] = dict()
		for time_unit in model_dict[weekday]:
			stop_id_dict[weekday][time_unit] = list()
			for stop_id in model_dict[weekday][time_unit]:
				stop_id_dict[weekday][time_unit].append(stop_id)
	return stop_id_dict



def routes_at_stop(model_dict, weekday, time_unit, stop):
	stop_data = model_dict[weekday][time_unit][stop]
	route_list = list()
	for quadruple in stop_data:
		route = quadruple[3]
		if route not in route_list:
			route_list.append(route)
	return [stop, route_list]

def routes_dict(model_dict):
	# make the framework
	r_dict = dict()
	for weekday in model_dict:
		r_dict[weekday] = dict()
		for time_unit in model_dict[weekday]:
			r_dict[weekday][time_unit] = dict()
	# populate the dictionary
	for weekday in model_dict:
		for time_unit in model_dict[weekday]:
			for stop in model_dict[weekday][time_unit]:
				stop_and_routes_list = routes_at_stop(model_dict, weekday, time_unit, stop)
				route_list = stop_and_routes_list[1]
				destination_dict = r_dict[weekday][time_unit]
				for route in route_list:
					if route not in destination_dict:
						destination_dict[route] = set()
					for other_route in route_list:
						destination_dict[route].add(other_route)
	# return
	return r_dict


if __name__ == "__main__":
	model_dict = data.get_model_data()
	r_dict = routes_dict(model_dict)
	for weekday in r_dict:
		for time_unit in r_dict[weekday]:
			for route in r_dict[weekday][time_unit]:
				print(weekday, time_unit, route)
				print(r_dict[weekday][time_unit][route])
				print("")