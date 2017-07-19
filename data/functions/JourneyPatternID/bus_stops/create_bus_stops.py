# imports
import os
import general
import merge_sort
import generate_routes
import generate_bus_stop


def create_files():
	file_names = general.list_of_csv_files()
	for file_name in file_names:
		# generate the source data
		the_journeys = generate_routes.routes(file_name)
		all_stops = generate_bus_stop.unique_stops(the_journeys)
		# create the object of interest
		bus_route = bus_stops(all_stops, the_journeys)
		# save the object of interest to file
		general.bsf_to_bsd()
		with open(file_name, "w") as destination:
			destination.write(",".join(bus_route))
		general.bsd_to_bsf()


if __name__ == "__main__":
	create_files()