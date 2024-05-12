import pandas as pd
import httpx
from typing import List
import csv

bing_maps_key = 'AqesDSP1QCJfuPJJ0PeaaRPGCFr2gou-EVTJEgM5_d_aNCw80OGn1BfVXAZRqvWk'

time_ls = []
fields = ['from','to','time']


def calculate_times(villages: List[str]):
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
                    # print(data)
                    time = data["resourceSets"][0]["resources"][0]["travelDuration"]
                    matrix[origin][destination] = time
                except httpx.HTTPStatusError as e:
                    print(f"Error calculating time from {origin} to {destination}: {e}")
                    matrix[origin][destination] = 0  # Use 0 or another placeholder value to indicate an error.

                # Append the result to the output file.
                # with open("time_putput.txt", "a") as f:
                #     if matrix[origin][destination] == 0:
                #         print(origin, "to", destination, ": Error", file=f)
                #     else:
                #         print(origin, "to", destination, ":", time, file=f)


                # Writing data to CSV file
                dict = {}
                if matrix[origin][destination] == 0:
                    dict['from']= origin
                    dict['to']= destination
                    dict['time']= 'Error'
                else:
                    dict['from']= origin
                    dict['to']= destination
                    dict['time']= time

                print(dict)

                time_ls.append(dict)

                with open('time_outputs.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.DictWriter(file, fieldnames = fields)   
                    writer.writeheader()
                    for row in time_ls:
                        writer.writerow(row)

                # with open("time_output.csv", "w", newline="") as csvfile:
                #     fieldnames = ['from', 'to', 'time']
                #     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                #     writer.writeheader()
                #     if matrix[origin][destination] == 0:
                #         writer.writerow({'from': origin, 'to': destination, 'time': 'Error'})
                #     else:
                #         writer.writerow({'from': origin, 'to': destination, 'time': time})

    return matrix





# Assuming the CSV file has a column named 'VILLAGES' with the village addresses.
df = pd.read_csv("input - Sheet1.csv")
village_addresses = df['VILLAGES'].tolist()
time_matrix = calculate_times(village_addresses)

# with open('time_outputs.csv', 'w', newline='', encoding='utf-8') as file:
#     writer = csv.DictWriter(file, fieldnames = fields)   
#     writer.writeheader()
#     for row in time_ls:
#         writer.writerow(row)

# Convert the time matrix to a DataFrame.
time_df = pd.DataFrame(time_matrix)

# Print the new DataFrame with the time matrix.
print(time_df)