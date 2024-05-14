BingMapsKey="AtS2Fs-Sm3fm-RPtqb9wDU5VB5cGImY_qIQXbd_Y-cojdSh_RCUDWRj8beBZRm-l"
import pandas as pd
import chardet
import csv 
import numpy as np
import requests
with open(r'C:\Users\Haresh\Projects\RouteXpert\models\village_name.csv', 'rb') as f:
    result = chardet.detect(f.read())


encoding = result['encoding']
print("yes")
df = pd.read_csv(r'C:\Users\Haresh\Projects\RouteXpert\models\village_name.csv', encoding=encoding)
coordinates=[]
for i in range(len(df)):
  locationQuery = df.iloc[i,:].values[0]
  print(locationQuery)
  api = f'http://dev.virtualearth.net/REST/v1/Locations?query={locationQuery}&key={BingMapsKey}'
  response = requests.get(api)
  if response.status_code!=200:
    print(response.json())
    coordinates.append("Error fetching location")

  resource = response.json()['resourceSets'][0]['resources']
  if resource == []:
    pass
    # coordinates.append((np.nan, np.nan)) 
  else:
    coordinates.append(resource[0]['point']['coordinates'])

print(coordinates)


print("Number of rows in village_name.csv:", df.shape[0])

filename = "output_coordinates.csv"

with open(filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    # writer.writerow(['Column 1', 'Column 2'])  # Writing header
    writer.writerows(coordinates)

print("CSV file has been created successfully.")