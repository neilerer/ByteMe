# imports
import general


# also use a dummy wait-time dictionary as a place holder so we are not constantly switching

def create_journey(stop_id, jpi, bus_stop_dict):
	possible_next = bus_stop_dict[stop_id]

# bus_stop_dict = general.next_stop_from_file()
# for item in bus_stop_dict:
# 	print(item)
# 	print(bus_stop_dict[item])
# 	print("")