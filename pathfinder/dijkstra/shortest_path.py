# imports
import general
import merge_sort
import data_conversion_routes_to_stops as dcrts


"""
been_list
- list of stop ids, all str

journey_id_list
- list of journey ids, all str

active_journey
- str value set to active journey

journies_dict
- {journey_id : [time, journey]}
-- journey_id is str
-- time is float
-- journy is list of stop details
--- stop details (start stop, next stop, next time, route)

"""

"""
Start
- set each tuple as a journey

- compare time of all journies and continue the journey with the lowest value

Ongoing
- for each tuple at stop, if not been, extend current journey, each as a new journey
-- remove old current journey

- if at destination, return that journey

- if cannot move and not at destination, remove from journies

- compare time of all journies and continue with the lowest value

"""


stop_dict = dcrts.get_bus_stop_data()
been_list = []
journey_id = 0
journey_id_list = []
journies_dict = dict()
shortest_path = None
found_shortest_path = False


def start_journey(start_stop_id, stop_dict, been_list, journey_id, journey_id_list, journies_dict):
	# record that we've been to this bus stop
	been_list.append(start_stop_id)
	# find the data we will use to start our journies
	list_of_next_stop_details = stop_dict[start_stop_id]
	# populate journies_dict
	for stop_detail in list_of_next_stop_details:
		next_stop_id = stop_detail[1]
		next_time = stop_detail[2]
		# check if we've already been there
		if next_stop_id not in been_list:
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			journies_dict[journey_id] = [next_time, [stop_detail]]
			# increment the journey_id
			journey_id += 1


def continue_journey(end_stop_id, stop_dict, been_list, journey_id, journey_id_list, journies_dict):
	# sort journies so we know which is the shortest
	journies_dict = merge_sort.merge_sort_journies_dict(journies_dict)
	# pop the shortest journey to extend and continue it
	starting_details = merge_sort.remove_first_entry_of_dict(journies_dict)
	journey_time = starting_details[0]
	journey_details = starting_details[1]
	start_stop_id = journey_details[-1][0]
	next_stop_id = journey_details[-1][1] # {0: [3.07, [(78, 77, 3.07, -3)]], 1: [21.93, [(78, 79, 21.93, 3)]]}
	# check if we are at the destination
	if start_stop_id == end_stop_id:
		found_shortest_path = True
		shortest_path = starting_details
	elif next_stop_id in been_list:
		pass
	else:
		been_list.append(next_stop_id)
		list_of_next_stop_details = stop_dict[next_stop_id]
		# populate journies_dict
		for stop_detail in list_of_next_stop_details:
			next_stop_id = stop_detail[1]
			next_time = stop_detail[2]
			# check if we've already been there
			if next_stop_id not in been_list:
				# record the journey_id
				journey_id_list.append(journey_id)
				# create the journey details
				journies_dict[journey_id] = [journey_time + next_time, journey_details.append(stop_detail)]
				# increment the journey_id
				journey_id += 1







if __name__ == "__main__":
	start_journey(78, stop_dict, been_list, journey_id, journey_id_list, journies_dict)
	print(journies_dict)
	continue_journey(stop_dict, been_list, journey_id, journey_id_list, journies_dict)