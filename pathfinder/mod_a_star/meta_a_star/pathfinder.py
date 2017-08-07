# imports
import data
import user_input
import shortest_path
import shortest_journey



# data
model_dict = data.get_model_data()
connections_dict = data.get_connections_dict()



if __name__ == "__main__":
	# testing user input
	start_stop_id =  400 #765
	end_stop_id = 600 #462 
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
	time_unit_connections_dict = shortest_path.get_time_unit_connections_dict(connections_dict, weekday, time_unit)
	print("Details of Path Possibilities")
	shortest_path_candidates = list()
	for pp in path_possibilities:
		start_route_id = pp[0]
		end_route_id = pp[1]
		shortest_path_candidates.append(shortest_path.find_shortest_path(start_route_id, end_route_id, time_unit_connections_dict))
	for sp_candidate in shortest_path_candidates:
		print(sp_candidate)
	print("")

	# test find_shortest_path_candidates_from_multiple_options
	print("Details of Reduced Path Possibilities")
	reduced_path_possibilities = shortest_path.find_shortest_path_candidates_from_multiple_options(path_possibilities, time_unit_connections_dict)
	for rpp in reduced_path_possibilities:
		print(rpp)
	print("")

	# test start_journey
	print("Start of Shortest Journey")
	for path in reduced_path_possibilities:
		journey_id_list = list()
		journies_dict = dict()
		start_sj = shortest_journey.start_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
		print(start_sj)
	print("")

	# test continue_journey
	print("First continuation of Shortest Journey")
	for path in reduced_path_possibilities:
		journey_id_list = list()
		journies_dict = dict()
		start_sj = shortest_journey.start_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
		first_cont_of_sj = shortest_journey.continue_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
		print(first_cont_of_sj)
	print("")

	# test find_shortest_journey
	print("Shortest Journey")
	for path in reduced_path_possibilities:
		journey_id_list = list()
		journies_dict = dict()
		sj = shortest_journey.find_shortest_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
		print(sj)
	print("")