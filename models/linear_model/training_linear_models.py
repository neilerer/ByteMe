import pandas as pd
from sklearn import linear_model
from sklearn.metrics import mean_squared_error
import numpy as np
import os
import glob
import pickle as pkl
import json

route_list=[]
model_metrics={}

for data_file in glob.glob("C:/Users/Conor/Desktop/Summer Project/Linear Model/clean_data/*.csv"):
	try:
		# only "0001" or "1001" routes for now
		if data_file[-14:-10]=="0001" or data_file[-14:-10]=="1001":
		
			route=data_file[-18:-14].lstrip('0')
			
		
			# getting current jpid
			jpid=data_file[-18:-10]
			print(jpid)
			
			#creating dataframe from cleaned data file
			df=pd.read_csv(data_file)
			
			# replacing '-' visibility entries with average visibility of the rest of the df
			avg_vis=np.mean((df[df['Visibility (km)']!='-'])['Visibility (km)'].astype(np.float32))
			df.loc[df['Visibility (km)']=='-','Visibility (km)']=avg_vis
			df['Visibility (km)']=df['Visibility (km)'].astype(np.float32)
			
			# replacing 'Calm' entries in wind speed with 0
			df.loc[df['Wind Speed (km/h)']=='Calm','Wind Speed (km/h)']=0
			df['Wind Speed (km/h)']=df['Wind Speed (km/h)'].astype(np.float32)
			
			# day of week and hour are categorical not continuous
			df['WeekDay']=df['WeekDay'].astype(object)
			df['Hours']=df['Hours'].astype(object)
			
			# swapping 64 bit fields for 32 bit ones
			for col in list(df):
				if df[col].dtype=='int64':
					df[col]=df[col].astype(np.int32)
				elif df[col].dtype=='float64':
					df[col]=df[col].astype(np.float32)
					
			# removing error cases
			df=df[df['Cumulative Time Taken']>=0]
			
			# changing weekday and hours to be categorical features
			df['WeekDay']=df['WeekDay'].astype(object)
			df['Hours']=df['Hours'].astype(object)
			
			
			""" BEGIN TRAINING MODEL """
			
			# stop 0 is starting point, so CTT is always zero
			linreg_df=df[df['StopSeq']!=0]
			
			# training model on full dataset
			X_train = linreg_df[['StopSeq','WeekDay','Hours']]
			y_train = linreg_df['Cumulative Time Taken']
			
			# initialising and training ols model
			ols=linear_model.LinearRegression()
			model=ols.fit(X_train,y_train)
			
			# adding model metrics to dictionary for evaluation purposes
			model_metrics[jpid]={}
			model_metrics[jpid]['r_square']=model.score(X_train, y_train)
			model_metrics[jpid]['rmse']=(mean_squared_error(y_train, model.predict(X_train)))**0.5
			
			# dumping model to pkl file
			pkl.dump(model,open('pickle_files/'+jpid+'.pkl','wb'),pkl.HIGHEST_PROTOCOL)
			
			# creating list of unique routes
			if route not in route_list:
				route_list.append(route)
	except:
		continue
		
with open("model_metrics.json","w",newline="") as metric_file:
	json.dump(model_metrics,metric_file)

with open('route_list','wb') as route_file:
	pkl.dump(route_list,route_file)
			
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	