# imports




def user_input(start_stop_id, end_stop_id, weekday, time_unit, model_dict):
	# find the appropriate data
	time_unit_dict = model_dict[weekday, time_unit]
	# get details
	start_details = time_unit_dict[start_stop_id]
	end_details = time_unit_dict[end_stop_id]
	return [start_details, end_details]

