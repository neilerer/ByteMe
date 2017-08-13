# imports
import data
import dijkstra



def pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict):
	journey_id_list = list()
	journies_dict = dict()
	been_set = set()
	the_shortest_journey = dijkstra.dijkstra(weekday, time_unit, start_stop_id, end_stop_id, model_dict, journey_id_list, journies_dict, been_set)
	return the_shortest_journey



if __name__ == "__main__":
	# data
	print("Loading the model data . . .")
	model_dict = data.get_model_data()

	# inputs
	start_stop_id =  807
	end_stop_id = 763
	weekday = 0
	time_unit = 10

	# test pathfinder
	print("")
	print("Pathfinder")
	the_shortest_journey = pathfinder(weekday, time_unit, start_stop_id, end_stop_id, model_dict)
	print(the_shortest_journey)