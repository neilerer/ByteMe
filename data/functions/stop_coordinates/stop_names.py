from geopy.geocoders import Nominatim
import json
geolocator = Nominatim()

with open("../../static_data/stop_coordinates.json") as file:
	coords_dict=json.load(file)

if False:
	result_dict={}
	count=0
	for stop in coords_dict:
		location = geolocator.reverse(str(coords_dict[stop][0])+","+str(coords_dict[stop][1]))		
		result_dict[stop]=[coords_dict[stop][0],coords_dict[stop][1],location.address]
		count+=1
		if count>100:
			break

	print(result_dict)
