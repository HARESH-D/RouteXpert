#importing modules
import random
import numpy as np
import math
import heapq
import pandas as pd
import sys
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import time
from itertools import chain
import openpyxl
import folium
import plotly

workbook = openpyxl.load_workbook(r"C:\Users\Haresh\Projects\RouteXpert\models\village_inputs.xlsx")
print(workbook)


#initializing input data
num_vehicles = 4
depot =  (9.926245401146815, 78.14286295767175)   #depot location

villages_list = []


sheet = workbook["village_inputs"]
for row in sheet.iter_rows(values_only=True):
    villages_list.append((row[0], row[1]))

villages_list = villages_list[:20]
time_matrix = np.load(r"C:\Users\Haresh\Projects\RouteXpert\models\time_matrix.npy")



df = pd.DataFrame(villages_list,columns=["x","y"])
print(df)
vehicle_visited_village=[[] for i in range(num_vehicles)]
max_num_villages = len(villages_list)
plot=[]

#training using kmeans

villages_list.pop(0)
# villages_list.pop(0)

print("villages_list",villages_list)
start_time = time.time()
kmeans = KMeans(n_clusters= num_vehicles,random_state=42)
kmeans.fit(df[["x", "y"]])
df['villages'] = kmeans.labels_
end_time = time.time()
duration = end_time - start_time
print("Duration for computation: ",duration)

for i in range(len(df)):
    data=df.iloc[i,:]
    vehicle_visited_village[int(data['villages'])].append((data['x'],data['y']))
    
for i in vehicle_visited_village:   
    i.insert(0,depot)

for i in range(len(vehicle_visited_village)):
    temp = vehicle_visited_village[i]
    temp.sort(key=lambda x:abs(x[0])+abs(x[1]))
    vehicle_visited_village[i]=temp

for i in vehicle_visited_village:   
    i.append(depot)


print("vehicle_visited_village", vehicle_visited_village)






