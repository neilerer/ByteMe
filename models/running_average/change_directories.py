#imports
import os



# jpi
def to_jpi():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID")

def from_jpi():
	os.chdir("../../../")
	os.chdir("models/running_average")



# sf
def to_sf():
	os.chdir("../../")
	os.chdir("data/data/JourneyPatternID/stop_format")

def from_sf():
	os.chdir("../../../../")
	os.chdir("models/running_average")