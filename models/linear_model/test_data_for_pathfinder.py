import pickle as pkl
import json
import pandas as pd
import glob
	
with open("../../data/static_data/jpids_and_stops.json") as jpids_and_stops:
	jpids_and_stops = json.load(jpids_and_stops)
	
result={}
for route_file in glob.glob("pickle_files/*.pkl"):
	route=route_file[-12:-4]
	print(route)
	
	with open("pickle_files/"+route+".pkl", 'rb') as model_file:
		model=pkl.load(model_file)

	result[route]={}
	for stopseq in range(len(jpids_and_stops[route])):
		for day in range(7):
			for hour in range(7,24):
				if stopseq==0:
					result[route][str(stopseq)+"-"+str(jpids_and_stops[route][stopseq])+"-"+str(day)+"-"+str(hour)]=0
				else:
					query_dict={'StopSeq':[stopseq],'WeekDay':[day],'Hours':[hour]}
					query_df=pd.DataFrame.from_dict(query_dict)
					query_df=query_df[['StopSeq','WeekDay','Hours']]
					result[route][str(stopseq)+"-"+str(jpids_and_stops[route][stopseq])+"-"+str(day)+"-"+str(hour)]=model.predict(query_df)[0]

with open("data_for_pathfinder.json","w",newline="") as file:
	json.dump(result,file)
				
