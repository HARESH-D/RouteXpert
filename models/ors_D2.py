import requests
import pandas as pd
import json
import numpy as np
import time

API_KEY = "AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk"
df= pd.read_csv('time_outputs.csv')
locations = []
for i in range(len(df)):
    lat=df.iloc[i,0]
    long=df.iloc[i,1]
    locations.append({'latitude':lat,'longitude':long})


def call_api(locations_group,end_group=None):
    if end_group == None:
        end_group = locations_group
    post_req=f'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={API_KEY}'
    body={"origins": locations_group,'destinations':end_group,"travelMode": 'Driving'}
    
    response = requests.post(post_req, json=body)
    if response.status_code!=200:
        return [[ float('inf') for i in range(len(locations_group)) ] for j in range(len(locations_group))]
    else:
        data = json.loads(response.text)
        matrix_raw = data['resourceSets'][0]['resources'][0]['results']
        matrix = [ [0 for i in range(len(df))] for j in range(len(df)) ]
        for i in matrix_raw:
            matrix[i['originIndex']][i['destinationIndex']] = i['travelDuration']
        return matrix

def generate_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = [[float('inf') for i in range(num_locations)] for j in range(num_locations)]


    groups = [locations[i:i+49] for i in range(0, num_locations, 49)]


    for i, grouprow in enumerate(groups):
        for j, groupcol in enumerate(groups):
            distance_matrix_group = call_api(grouprow,groupcol)
            start_row = i * 49
            end_row = min(start_row + 49, num_locations)
            start_col = j * 49
            end_col = min(start_col + 49, num_locations)
            for a in range(0,end_row-start_row):
                for b in range(0,end_col-start_col):
                    # print(i,j,a,b)
                    distance_matrix[start_row+a][start_col+b] = distance_matrix_group[a][b]
            
    return distance_matrix


d2_matrix = generate_distance_matrix(locations)
d2_matrix = np.array(d2_matrix)
np.save('d1_matrix.npy',d2_matrix)

print("length: ",len(d2_matrix))
print(d2_matrix)
