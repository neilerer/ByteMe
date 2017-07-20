# imports
import os
import general


# DIRECTORY CHANGES
#
def dc_to_bsd():
	os.chdir("../../../")
	os.chdir("data/JourneyPatternID/bus_stops")
def bsd_to_dc():
	os.chdir("../../../")
	os.chdir("pathfinder/data_collection")