"""Finding the closest neighbouring bus stops for each bus stop"""

import json 
from math import sin, cos, sqrt, atan2, radians

def locations_within_distance(point,comparables,distance):
	"""Function takes co-ordinates of a point, a dictionary with other coordinates, and a distance threshold (metres)"""
	# https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
	earth_radius=6371000 # in kilometres
	stops_within_distance=[]
	for location in comparables:
		# calculating distance
		
		point_radians=[radians(float(point[0])),radians(float(point[1]))]
		location_coords_radians=[radians(float(comparables[location][0])),radians(float(comparables[location][1]))]
		lat_difference=point_radians[0]-location_coords_radians[0]
		long_difference=point_radians[1]-location_coords_radians[1]
		a = sin(lat_difference/ 2) ** 2 + cos(float(point_radians[0])) * cos(float(location_coords_radians[0])) * sin(long_difference/ 2) ** 2
		c = 2 * atan2(sqrt(a), sqrt(1 - a))

		if earth_radius*c<distance:
			stops_within_distance.append(location)

	return stops_within_distance

with open("stop_info.json") as stop_file:
	stop_coordinates = json.load(stop_file)

print("loaded in json file")

for key in stop_coordinates:
	stop_coordinates[key]=stop_coordinates[key][:4]
	print(key, stop_coordinates[key])

new={}
for stop in stop_coordinates:
	new[stop]=stop_coordinates[stop]
	new[stop].append(locations_within_distance([stop_coordinates[stop][0],stop_coordinates[stop][1]],stop_coordinates,75))
	print("calculated nearest stops for stop",stop)

numbers=[]
for stop in new:
	numbers.append(len(new[stop][4]))

print(numbers, sum(numbers)/float(len(numbers)), max(numbers))

with open('stop_info.json','w') as result_file:
	json.dump(new,result_file)