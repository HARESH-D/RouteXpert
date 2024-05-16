import requests
import pandas as pd
import json
import numpy as np
import time

API_KEY = "AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk"
df= pd.read_csv('village_inputs.csv')
df2= pd.read_csv('warehouse_inputs.csv')

locations = []
for i in range(len(df)):
    lat=df.iloc[i,0]
    long=df.iloc[i,1]
    locations.append({'latitude':lat,'longitude':long})


def call_api(locations_group,end_group=None):
    if end_group == None:
        end_group = locations_group
    post_req=f'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={API_KEY}'
    body={"origins": [{"latitude":9.926181981935146, "longitude":78.1428200388285}],'destinations':locations_group,"travelMode": 'Driving'}
    response = requests.post(post_req, json=body)
    if response.status_code!=200:
        print(response.text)
        return [[ float('inf') for i in range(len(locations_group)) ] for j in range(len(locations_group))]
    else:
        data = json.loads(response.text)
        matrix_raw = data['resourceSets'][0]['resources'][0]['results']
        matrix = [ [0 for i in range(len(df))] for j in range(len(df)) ]
        for i in matrix_raw:
            matrix[i['originIndex']][i['destinationIndex']] = i['travelDuration']
        return matrix



d1_matrix = call_api(locations)
time_matrix = np.array(d1_matrix)
np.save('d1_matrix.npy',time_matrix)

print("length: ",len(time_matrix))
print(time_matrix)
