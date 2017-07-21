# imports
import general
import intersections


def create_intersections():
	jpi_intersections = intersections.get_all_intersections()
	general.dc_to_i()
	with open("jpi_intersections.txt", "w") as destination:
		for jpi in jpi_intersections:
			key = jpi
			value = jpi_intersections[jpi]
			destination.write(key, value, "\n")
	general.i_to_dc()


if __name__ == "__main__":
	create_intersections()