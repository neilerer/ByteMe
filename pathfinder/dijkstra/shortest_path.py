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
-- also, if at destination, return that journey

Ongoing
- for each tuple at stop, if not been, extend current journey, each as a new journey
-- remove old current journey

- compare time of all journies and continue with the lowest value
-- also, if at destination, return that journey
"""


stop_dict = dcrts.get_bus_stop_data()
been_list = []
journey_id_list = []
active_journey = 0
journies_dict = dict()

def continue_journey(journey_id, stop_id, stop_dict, been_list, journey_id_list, journies_dict):
	journey_to_extend = journies_dict[journey_id]



def continue_journey(journey_id, stop_id, stop_dict, journies_list, been_list):
	list_of_stop_details = stop_dict[stop_id]
	for stop_detail in list_of_stop_details:
		next_stop = stop_detail[1]
		next_time = stop_detail[2]
		next_route = stop_detail[3]
		if next_stop in been_list:
			pass
		else:
			pass