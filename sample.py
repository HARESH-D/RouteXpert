import pandas as pd
import httpx
from typing import List

bing_maps_key = 'AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk'

def calculate_distances(villages: List[str]):
    matrix = {}
    m = villages
    for i, origin in enumerate(m):
        matrix[origin] = {}
        for j, destination in enumerate(villages):
            if i == j:
                matrix[origin][destination] = 0
            elif matrix.get(destination, {}).get(origin) is not None:
                matrix[origin][destination] = matrix[destination][origin]
            else:


                response = httpx.get(
                    "http://dev.virtualearth.net/REST/v1/Routes/Driving",
                    params={
                        "wp.0": origin,
                        "wp.1": destination,
                        "key": bing_maps_key
                    }
                )
                response.raise_for_status()
                data = response.json()
                distance = data["resourceSets"][0]["resources"][0]["travelDistance"]
                matrix[origin][destination] = distance
                
                with open("output.txt", "a") as f:
                    print(origin, "to", destination, ":", distance, file=f)


    return matrix

# Assuming the CSV file has a column named 'Address' with the village addresses.
df = pd.read_csv("input - Sheet1.csv")
village_addresses = df['VILLAGES'].tolist()  # Replace 'Address' with the actual column name.
distance_matrix = calculate_distances(village_addresses)

# Convert the distance matrix to a DataFrame.
distance_df = pd.DataFrame(distance_matrix)

# Print the new DataFrame with the distance matrix.
print(distance_df)