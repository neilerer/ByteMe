"""Adding the routes served by each StopID to the stop_info file for Django"""

import json

with open("jpids_and_stops.json") as file:
	jpids_and_stops=json.load(file)
	
with open("stop_coordinates_with_names.json") as file:
	stop_info=json.load(file)

for stop in stop_info:
	stop_info[stop].append([])
	for jpid in jpids_and_stops:
		if stop in jpids_and_stops[jpid]:
			if " "+jpid[0:4].lstrip("0") not in stop_info[stop][3]:
				stop_info[stop][3].append(" "+jpid[0:4].lstrip("0"))

for stop in stop_info:
	stop_info[stop][3]=sorted(stop_info[stop][3])
	
with open("stop_info.json","w",newline="") as file:
	json.dump(stop_info,file)
				