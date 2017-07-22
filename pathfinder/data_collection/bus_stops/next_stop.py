# import
import general
import source_data


def bus_stops(bus_stop_dict):
	# holder for return values
	bus_stop_unique_values = set()
	# iterate over the values in each element of the dictionary
	for jpi in bus_stop_dict:
		for stop in bus_stop_dict[jpi]:
			bus_stop_unique_values.add(stop)
	# return
	return list(bus_stop_unique_values)


def next_for_stop_id(stop_id, bus_stop_dict):
	next_dict = {}
	for jpi in bus_stop_dict:
		try:
			index = bus_stop_dict[jpi].index(stop_id) + 1
			key = (bus_stop_dict[jpi][index], jpi)
			next_dict[key] = False
		except:
			pass
	return (stop_id, next_dict)


def next_for_all():
	bus_stop_dict = source_data.jpi_dictionary()
	next_dict = {}
	bus_stop_unique_values = bus_stops(bus_stop_dict)
	for stop_id in bus_stop_unique_values:
		data = next_for_stop_id(stop_id, bus_stop_dict)
		next_dict[data[0]] = data[1]
	return next_dict

my_dict = next_for_all()
for item in my_dict:
	print(item)
	print(my_dict[item])
	print("")