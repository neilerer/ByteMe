import geopy
import json
geolocator = geopy.Nominatim()

with open("../../static_data/stop_coordinates.json") as file:
	coords_dict=json.load(file)

with open("../../static_data/stop_coordinates_with_names.json") as namefile:
	names_dict=json.load(namefile)

for key in names_dict:
	print(key,names_dict[key])
	
if False:
	result_dict={}
	for stop in coords_dict:
		if stop not in names_dict:
			try:
				location = geolocator.reverse(str(coords_dict[stop][0])+","+str(coords_dict[stop][1]))		
				result_dict[stop]=[coords_dict[stop][0],coords_dict[stop][1],location.address]
			except:
				print("except block")
				continue
			
	with open("../../static_data/stop_coordinates_with_names.json","w",newline="") as result_file:
				json.dump(result_dict,result_file)



