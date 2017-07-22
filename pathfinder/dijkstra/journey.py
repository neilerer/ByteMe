# imports
import general

bus_stop_dict = general.next_stop_from_file()
for item in bus_stop_dict:
	print(item)
	print(bus_stop_dict[item])
	print("")