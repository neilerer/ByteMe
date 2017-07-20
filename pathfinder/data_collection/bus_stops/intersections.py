# imports
import general
import source_data


# returns a tuple with the secondary_jpi and the stops on it that intersect with the primary_jpi
def get_intersection_pairwise(primary_jpi, secondary_jpi, bus_stop_dict):
	# data objects
	intersection_list = []
	primary_list = bus_stop_dict[primary_jpi]
	secondary_list = bus_stop_dict[secondary_jpi]
	# iteration to populate intersection_list
	for stop_id in primary_list:
		if stop_id in secondary_list:
			intersection_list.append(stop_id)
	# return
	return (secondary_jpi, intersection_list)

# generates a tuple of the primary_jpi and a dictionary of each connected jpi and the stops of intersection
def get_intersection_all_pairwise(primary_jpi, bus_stop_dict):
	all_pairwise_intersections = {}
	for jpi in bus_stop_dict:
		if jpi == primary_jpi:
			pass
		else:
			intersection_tuple = get_intersection_pairwise(primary_jpi, jpi, bus_stop_dict)
			if intersection_tuple[1] == []:
				pass
			else:
				all_pairwise_intersections[jpi] = intersection_tuple[1]
	return all_pairwise_intersections

bus_stop_dict = source_data.jpi_dictionary()
primary_jpi = "00010001"
secondary_jpi = "00011001"
# print(get_intersection_pairwise(primary_jpi, secondary_jpi, bus_stop_dict))
my_result = get_intersection_all_pairwise(primary_jpi, bus_stop_dict)
for item in get_intersection_all_pairwise(primary_jpi, bus_stop_dict):
	print(item)
	print(my_result[item])
	print("")