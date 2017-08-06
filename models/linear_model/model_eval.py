import json
import pickle as pkl

with open("model_metrics.json") as file:
	metrics=json.load(file)
if False:
	retraining_set=[]
	for key in metrics:
		if metrics[key]['r_square']<.85:
			retraining_set.append(key)
		
	pkl.dump(retraining_set,open('jpids_for_retraining.pkl','wb'),pkl.HIGHEST_PROTOCOL)

	missing_models=[]
	for key in metrics:
		if key[-4:]=="0001":
			opp_dir=key[:4]+"1001"
			try: 
				metrics[opp_dir]
			except:
				missing_models.append(opp_dir)
				
		elif key[-4:]=="1001":
			opp_dir=key[:4]+"0001"
			try: 
				metrics[opp_dir]
			except:
				missing_models.append(opp_dir)

	pkl.dump(missing_models,open('missing_model_directions.pkl','wb'),pkl.HIGHEST_PROTOCOL)


with open("jpids_for_retraining.pkl", "rb") as retrain_file: # loading pickle file with routes
	routes=pkl.load(retrain_file)
	print("For retraining:","\n",routes)
with open("missing_model_directions.pkl", "rb") as missing_file: # loading pickle file with routes
	miss_routes=pkl.load(missing_file)
	print("Missing routes:","\n",miss_routes)