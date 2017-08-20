# imports



def target_route_goes_first(journies_dict, target_routes):
	# [True, {1: [0.00, [(start_stop_id, end_stop_id, 0.00, "n/a")]]}]
	# data
	return_dict = dict()
	heuristic_list = list()
	secondary_list = list()
	# iterate over each journey in journies_dict
	for jid in journies_dict:
		# unpack the data
		value = journies_dict[jid]
		details = value[1]
		quadruple = details[-1]
		route = quadruple[3]
		# if the journey is on the target route, put it at the front of the line
		if route in target_routes:
			heuristic_list.append(jid)
		else:
			secondary_list.append(jid)
	# return
	if len(heuristic_list) > 0:
		for target_jid in heuristic_list:
			return_dict[target_jid] = journies_dict[target_jid]
		for target_jid in secondary_list:
			return_dict[target_jid] = journies_dict[target_jid]
		return return_dict
	else:
		return journies_dict


	# first_list = list()
	# second_list = list()
	# return_dict = dict()
	# # iterate over each journey in journies_dict
	# for jid in journies_dict:
	# 	# unpack the data
	# 	value = journies_dict[jid]
	# 	details = value[1]
	# 	quadruple = details[-1]
	# 	route = quadruple[3]
	# 	# if the journey is on the target route, put it at the front of the line
	# 	if route in target_routes:
	# 		first_list.append(jid)
	# 	else:
	# 		second_list.append(jid)
	# 	# populate return_dict
	# 	if len(first_list) > 0:
	# 		for jid in first_list:
	# 			return_dict[jid] = journies_dict[jid]
	# 	else:
	# 		for jp in se
	# # return
	# return return_dict



def create_target_routes(stop, stop_dict):
	target_routes = set()
	data = stop_dict[stop]
	for quadruple in data:
		target_routes.add(quadruple[3])
	return list(target_routes)