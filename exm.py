import pandas as pd
import httpx
from typing import List

bing_maps_key = 'AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk'

def calculate_distances(villages: List[str]):
    matrix = {}
    for i, origin in enumerate(villages):
        matrix[origin] = {}
        for j, destination in enumerate(villages):
            if i == j:
                matrix[origin][destination] = 0
            elif matrix.get(destination, {}).get(origin) is not None:
                matrix[origin][destination] = matrix[destination][origin]
            else:
                try:
                    response = httpx.get(
                        "https://dev.virtualearth.net/REST/v1/Routes/Driving",
                        params={
                            "wp.0": origin,
                            "wp.1": destination,
                            "key": bing_maps_key
                        }
                    )
                    response.raise_for_status()
                    data = response.json()
                    print(data)
                    distance = data["resourceSets"][0]["resources"][0]["travelDistance"]
                    matrix[origin][destination] = distance
                except httpx.HTTPStatusError as e:
                    print(f"Error calculating distance from {origin} to {destination}: {e}")
                    matrix[origin][destination] = 0  # Use 0 or another placeholder value to indicate an error.

                # Append the result to the output file.
                with open("output.txt", "a") as f:
                    if matrix[origin][destination] == 0:
                        print(origin, "to", destination, ": Error", file=f)
                    else:
                        print(origin, "to", destination, ":", distance, file=f)

    return matrix

# Assuming the CSV file has a column named 'VILLAGES' with the village addresses.
df = pd.read_csv("input - Sheet1.csv")
village_addresses = df['VILLAGES'].tolist()
distance_matrix = calculate_distances(village_addresses)

# Convert the distance matrix to a DataFrame.
distance_df = pd.DataFrame(distance_matrix)

# Print the new DataFrame with the distance matrix.
print(distance_df)