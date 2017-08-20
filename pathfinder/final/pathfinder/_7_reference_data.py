import _0_0_data as data


def stops_by_weekday_and_time_unit():
	output_dict = dict()
	stop_dict = data.get_pickle_file("stop_dict.p")
	for weekday in stop_dict:
		output_dict[weekday] = dict()
		for time_unit in stop_dict[weekday]:
			output_dict[weekday][time_unit] = list()
			for stop in stop_dict[weekday][time_unit]:
				output_dict[weekday][time_unit].append(stop)
	return output_dict


def check_stop(stops, stop_id):
	for weekday in stops:
		print("Checking {}".format(weekday))
		for time_unit in stops[weekday]:
			print("Checking hour {}".format(time_unit))
			if stop_id in stops[weekday][time_unit]:
				print("Found: {} is in {} at {}".format(stop_id, weekday, time_unit))
			else:
				print("Not Found: {} is not in {} at {}".format(stop_id, weekday, time_unit))
		print("")




if __name__ == "__main__":
	# stops = stops_by_weekday_and_time_unit()
	# check_stop(stops, 807)

	ctt_dict = data.get_pickle_file("ctt_dict.p")

	for weekday in ctt_dict:
		for time_unit in ctt_dict[weekday]:
			for route in ctt_dict[weekday][time_unit]:
				print(route)
				print(ctt_dict[weekday][time_unit][route])