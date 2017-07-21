# import
import general
import source_data


def bus_stops():
	bus_stop_dict = source_data.jpi_dictionary()
	bus_stop_unique_values = set()
	for jpi in bus_stop_dict:
		for stop in bus_stop_dict[jpi]:
			bus_stop_unique_values.add(stop)
	bus_stop_unique_values = list(bus_stop_unique_values)
	bus_stop_unique_values.sort()
	return bus_stop_unique_values

print(bus_stops())