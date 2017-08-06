# imports
import data
import user_input



# data
model_dict = data.get_model_data()


if __name__ == "__main__":
	# testing user input
	start_stop_id = 400
	end_stop_id = 600
	weekday = 0
	time_unit = 10
	journey_details = user_input.user_input(start_stop_id, end_stop_id, weekday, time_unit, model_dict)
	start_details = journey_details[0]
	end_details = journey_details[1]
	print("Start Details")
	for quadruple in start_details:
		print(quadruple)
	print("")
	print("End Details")
	for quadruple in end_details:
		print(quadruple)
	print("")

	# testing path_possibilities
	user_input.path_possibilities(journey_details)
	print("Path Possibilities")
	for pp in user_input:
		print(pp)
	print("")