# imports
import pickle
import general
import intersections


def intersections_to_file():
	jpi_intersections = intersections.get_all_intersections()
	general.dc_to_i()
	with open("jpi_intersections.p", "w") as destination:
		pickle.dump(jpi_intersections, destination)
	general.i_to_dc()


if __name__ == "__main__":
	intersections_to_file()