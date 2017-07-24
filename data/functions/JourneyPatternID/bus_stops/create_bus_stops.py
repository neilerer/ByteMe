# imports
import os
import general
import merge_sort
import generate_routes
import bayes_bus_stops


def create_files():
	file_names = general.list_of_csv_files()
	for file_name in file_names:
		# program checking
		print(file_name)
		# generate the source data
		the_journeys = generate_routes.routes(file_name)
		all_stops = bayes_bus_stops.unique_stops(the_journeys)
		neighbours_dict = bayes_bus_stops.left_neighbours_dict(the_journeys, all_stops)
		# create the object of interest
		bus_route = bayes_bus_stops.generate_bus_stops(neighbours_dict)
		if bus_route is False:
			continue
		# save the object of interest to file
		general.bsf_to_bsd()
		with open(file_name, "w") as destination:
			destination.write(",".join(bus_route))
		general.bsd_to_bsf()


if __name__ == "__main__":
	create_files()