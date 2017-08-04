import geopy
import json
from time import sleep

geolocator = geopy.Nominatim()

with open("stop_coordinates.json") as file:
	coords_dict=json.load(file)

with open("stop_coordinates_with_names.json") as namefile:
	result_dict=json.load(namefile)

if False: # code was used to query geopy for the name of each bus stop location
	new_stops=[]
	for stop in coords_dict:
		if stop not in result_dict:
			new_stops.append(stop)


	print("BEFORE:",len(result_dict))

	for stop in new_stops:
		sleep(1)
		if stop not in result_dict:
			try:
				location = geolocator.reverse(str(coords_dict[stop][0])+","+str(coords_dict[stop][1]))		
				result_dict[stop]=[coords_dict[stop][0],coords_dict[stop][1],location.address]
				print("added new stop")
			except:
				with open("stop_coordinates_with_names.json","w",newline="") as result_file:
					json.dump(result_dict,result_file)
				break
				
	with open("stop_coordinates_with_names.json","w",newline="") as result_file:
					json.dump(result_dict,result_file)

	print("AFTER:",len(result_dict))

for stop in result_dict: # chopping off the end of the result
	split_list=result_dict[stop][2].split(",")
	result_dict[stop][2]=",".join(split_list[:4])

with open("stop_coordinates_with_names.json","w",newline="") as result_file:
					json.dump(result_dict,result_file)