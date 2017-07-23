# imports
import general



# wait_time_dict assumed to match time period of bus_stop_dict and contain stop_id:{jpi:t, . . . } for each stop_id

def journey_start(journey_id, stop_id, bus_stop_dict, wait_time_dict, journies_dict):
	# obtain the source information
	next_dict = bus_stop_dict[stop_id]
	wait_dict = wait_time_dict[stop_id]
	# iteratively populate journies
	for next_stop in next_dict:
		# articulate the bus_stop_dict_entries
		next_stop_id = next_stop[0]
		jpi = next_stop[1]
		journey_time = next_dict[next_stop]
		# articulate the wait_time_dict entries: this is time spent waiting at stop_id for the relevant jpi bus
		wait_time = wait_dict[jpi]
		# create the first entry
		first_entry = (journey_id, stop_id, jpi, 0)
		# add the first entry
		journies_dict[journey_id] = [first_entry]
		# create the second entry
		second_entry = (journey_id, next_stop_id, jpi, wait_time + journey_time)
		# add the second entry
		journies_dict[journey_id].append(second_entry)
		# increment the journey_id
		journey_id += 1


# bus_stop_dict = general.next_stop_from_file()
# for item in bus_stop_dict:
# 	print(item)
# 	print(bus_stop_dict[item])
# 	print("")