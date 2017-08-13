import glob
import os
import json
import csv

ordered_bus_lists={}
for file in glob.glob("*.csv"):
	reader=csv.reader(open(file))
	line=next(reader)
	ordered_bus_lists[file[:-4]]=line

with open('routes_and_stops.json','w') as result_file:
	json.dump(ordered_bus_lists,result_file)
