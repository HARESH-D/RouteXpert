import requests
import pandas as pd
import json
import numpy as np

# Set the ORS API endpoint and API key (free tier available)
ORS_API_ENDPOINT = "https://api.openrouteservice.org/v2/matrix/driving-car"
API_KEY = "AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk"



df= pd.read_csv('village_inputs.csv')
body={"origins": [],"travelMode": 'Driving'}
for i in range(len(df)):
    lat=df.iloc[i,0]
    long=df.iloc[i,1]
    body['origins'].append({'latitude':lat,'longitude':long})
    
    
print(body)

post_req=f'https://dev.virtualearth.net/REST/v1/Routes/DistanceMatrix?key={API_KEY}'

response = requests.post(post_req, json=body)
print(response.status_code)
data = json.loads(response.text)
matrix_raw = data['resourceSets'][0]['resources'][0]['results']

matrix = [ [0 for i in range(len(df))] for j in range(len(df)) ]
for i in matrix_raw:
    matrix[i['originIndex']][i['destinationIndex']] = i['travelDuration']

print(matrix)
    
    
np.save('my_list.npy', matrix)

