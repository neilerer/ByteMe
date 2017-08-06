# imports
import data
import user_input
import shortest_path



# data
model_dict = data.get_model_data()
connections_dict = data.get_connections_dict()


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
	path_possibilities = user_input.path_possibilities(journey_details)
	print("Path Possibilities")
	for pp in path_possibilities:
		print(pp)
	print("")

	# testing find_shortest_path
	time_unit_connections_dict = get_time_unit_connections_dict(connections_dict, weekday, time_unit)
	print("Details of Path Possibilities")
	for pp in path_possibilities:
		start_route_id = pp[0]
		end_route_id = pp[1]
		print(find_shortest_path(start_route_id, end_route_id, time_unit_connections_dict))
	print("")