# imports
import data
import user_input
import shortest_path
import shortest_journey

def pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict, connections_dict):
	# user_input
	journey_details = user_input.user_input(start_stop_id, end_stop_id, weekday, time_unit, model_dict)
	start_details = journey_details[0]
	end_details = journey_details[1]
	# path_possibilities
	path_possibilities = user_input.path_possibilities(journey_details)
	# time_unit_connections_dict
	time_unit_connections_dict = shortest_path.get_time_unit_connections_dict(connections_dict, weekday, time_unit)
	# reduced_path_possibilities
	reduced_path_possibilities = shortest_path.find_shortest_path_candidates_from_multiple_options(path_possibilities, time_unit_connections_dict)
	# shorest_journey
	the_shortest_journey = [None, None, "There is no bus journey from {} to {}".format(start_stop_id, end_stop_id)]
	for path in reduced_path_possibilities:
		journey_id_list = list()
		journies_dict = dict()
		sj = shortest_journey.find_shortest_journey(weekday, time_unit, start_stop_id, end_stop_id, path, model_dict, journey_id_list, journies_dict)
		for journey_id in sj:
			sj_details = sj[journey_id]
			if sj_details[0] == None:
				pass
			else:
				if the_shortest_journey[0] is None:
					the_shortest_journey = sj_details
				else:
					if sj_details[0] < the_shortest_journey[0]:
						the_shortest_journey = sj_details
	return the_shortest_journey
