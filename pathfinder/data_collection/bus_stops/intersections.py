# imports
import general
import source_data


def get_intersection_pairwise(primary_jpi, secondary_jpi, bus_stop_dict):
	# data objects
	intersection_list = []
	primary_list = bus_stop_dict[primary_jpi]
	secondary_list = bus_stop_dict[secondary_jpi]
	# iteration to populate intersection_list
	for stop_id in primary_list:
		if stop_id in secondary_list:
			intersection_list.append(stop_id)
	return (secondary_jpi, intersection_list)

def get_intersection_all_pairwise(primary_jpi, bus_stop_dict):
	all_pairwise_intersections = {}
	for jpi in bus_stop_dict:
		if jpi == primary_jpi:
			pass
		else:
			intersection_tuple = get_intersection_pairwise(primary_jpi, jpi, bus_stop_dict)
			all_pairwise_intersections[jpi] = intersection_tuple[1]
	return (primary_jpi, all_pairwise_intersections)

bus_stop_dict = source_data.jpi_dictionary()
primary_jpi = "00010001"
secondary_jpi = "00011001"
print(get_intersection_pairwise(primary_jpi, secondary_jpi, bus_stop_dict))