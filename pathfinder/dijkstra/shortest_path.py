# imports
import general
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


def start_journey(stop_id, stop_dict, been_list, journey_id, journey_id_list, journies_dict):
	# record that we've been to this bus stop
	been_list.append(stop_id)
	# find the data we will use to start our journies
	list_of_next_stop_details = stop_dict[stop_id]
	# populate journies_dict
	for stop_detail in list_of_next_stop_details:
		# check if we've already been there
		if stop_detail[1] not in been_list:
			# record the journey_id
			journey_id_list.append(journey_id)
			# create the journey details
			journies_dict[journey_id] = stop_detail
			# increment the journey_id
			journey_id += 1

start_journey(78, stop_dict, been_list, journey_id, journey_id_list, journies_dict)
print(journies_dict)