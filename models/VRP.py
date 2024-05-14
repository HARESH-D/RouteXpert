import random
import numpy as np
import math
import heapq
import pandas as pd
import sys

import matplotlib.pyplot as plt
import time

import plotly.graph_objects as go
from itertools import chain
import openpyxl

sys.setrecursionlimit(10000000)


workbook = openpyxl.load_workbook('village_inputs.xlsx')

villages_list = []
sheet = workbook["village_inputs"]
for row in sheet.iter_rows(values_only=True):
    villages_list.append((row[0], row[1]))


# Transport location details 
villages_list = villages_list[:100]
max_num_villages = len(villages_list)


# Warehouse details 
depot_location = [(9.925485, 78.126581)]
village_product_demand = [(random.randint(*(0, 5)), random.randint(*(0, 5)), random.randint(*(0, 5))) for _ in range(max_num_villages)]


# Transport equipment details 
num_vehicles = 4
vehicle_max_load = [300, 200, 100, 100]
vehicles_initial_loc = [(20.5937, 78.9629) for i in range(num_vehicles)]


if num_vehicles != len(vehicle_max_load):
    print("Error vehicle_max_load !!")
    
    
    
########################### Time Matix ###########################

D1 = np.load("D1.npy").T        #D1 - vehicle/warehouse location to villages
D2 = np.load("D2.npy")          #D2[village1] to [village2]
D3 = D1                         #D3[village][depot]




#################################################################






def plot_(plot):
    # Create indices
    indices = range(len(plot))

    # Plot values against indices
    plt.plot(indices, plot)

    # Add labels and title
    plt.xlabel('Episodes')
    plt.ylabel('Rewards')
    plt.title('Episodes vs Rewards Plot')

    # Show the plot
    plt.show()



#  initial Order allocation----------------------------------------------------------------
Q_table = np.zeros((max_num_villages, max_num_villages))
episilon = 1.0
temperature = 0.7
gamma = 0.09  # Discount factor
alpha = 0.9  # Learning rate
num_episodes = 500
plot=[]






def action_selection(state_village,episilon, decay_rate = 0.99):
    while True:
        a = np.argsort(temp_Q[state_village])[:2]
        if temp_Q[state_village,a[0]]==temp_Q[state_village,a[1]]:
            action = random.choice(a)
        else:
            action = np.argmin(temp_Q[state_village])

        if action != state_village:
                break

    return action


def clipped_exp(val):
    return np.exp(np.clip(val, -1000, 1000))

def softmax(q_values, temperature=temperature):
    exponents = clipped_exp(q_values / temperature)
    return exponents / np.sum(exponents)

def crude_probabilistic_policy(q_values) -> int:
    probabilities = softmax(q_values)
    return np.random.choice(np.arange(len(q_values)), p=probabilities)

def action_selection_probability(state_village):
    action = crude_probabilistic_policy(temp_Q[state_village, :])
    if action == state_village:
        action = crude_probabilistic_policy(temp_Q[state_village, :])
    return action

def soft_state_value_function(q_values, temperature):
    return temperature * np.log( np.mean( clipped_exp(q_values / temperature) ) )

def pi_maxent(q_values, temperature):
    return clipped_exp( (q_values - soft_state_value_function(q_values, temperature)) / temperature)

def sql_policy(q_values, temperature):
    pi = pi_maxent(q_values, temperature)
    return crude_probabilistic_policy(pi), pi

def action_selection_SQL(state_village):
    while True:
        action, pi = sql_policy(temp_Q[state_village,:],temperature=1.)
        if action != state_village:
            break
    return action

print("villages_list",villages_list)
print("Initialization Over\n")
#  initial Order allocation----------------------------------------------------------------




start_time = time.time()

for episode in range(num_episodes):

    cumm = 0
    temp_D1 = D1.copy()
    temp_D2 = D2.copy()  
    temp_Q = Q_table.copy()

    finished_tasks = [] 
    vehicle_dist_lst = [0 for _ in range(len(vehicles_initial_loc))]

    vehicle_load_lst = vehicle_max_load.copy()


    vehicle_last_visited_village = [0 for _ in range(len(vehicles_initial_loc))]
    vehicle_visited_village = [[] for _ in range(len(vehicles_initial_loc))]
    

    print("\nEpisode", episode)


    for vehicle_i in range(len(vehicles_initial_loc)):

        state_village = np.argmin(temp_D1[vehicle_i])       #D1[vehicle_index][state_villagendex]

        vehicle_visited_village[vehicle_i].append(villages_list[state_village])

        reward = D1[vehicle_i][state_village] 

        finished_tasks.append(villages_list[state_village])
        vehicle_dist_lst[vehicle_i] += reward
        vehicle_last_visited_village[vehicle_i] = villages_list[state_village]

        vehicle_load_lst[vehicle_i] -= sum(village_product_demand[state_village])

        temp_D2[state_village, :], temp_D2[:, state_village] = np.inf, np.inf
        temp_D1[:, state_village] = np.inf
        temp_Q[:, state_village] = -np.inf 


    while(len(finished_tasks)!=max_num_villages):

        vehicle_i = vehicle_dist_lst.index(min(vehicle_dist_lst)) 
        
        state_village = villages_list.index(vehicle_last_visited_village[vehicle_i])
        

        # action_village = action_selection(state_village, episilon)
        # action_village = action_selection_probability(state_village)
        action_village = action_selection_SQL(state_village)
        
        if sum(village_product_demand[action_village]) > vehicle_load_lst[vehicle_i]:
            # D1[vehicle_i][state_village] + D1[vehicle_i][action_village]
            nearest_depot = np.argmin(D3[state_village])
            
            reward = D3[state_village][nearest_depot] + D3[action_village][nearest_depot]

            
            vehicle_load_lst[vehicle_i] = vehicle_max_load[vehicle_i]
            vehicle_visited_village[vehicle_i].append(villages_list[nearest_depot])
            vehicle_load_lst[vehicle_i] -= sum(village_product_demand[state_village])

        else:
            reward = D2[state_village][action_village]
            vehicle_load_lst[vehicle_i] -= sum(village_product_demand[state_village])

        Q_table[state_village, action_village] += alpha * (-reward + gamma * soft_state_value_function(Q_table[action_village], temperature) - Q_table[state_village, action_village])
        temp_Q[state_village, action_village] += alpha * (-reward + gamma * soft_state_value_function(temp_Q[action_village], temperature) - temp_Q[state_village, action_village])

        temp_D2[action_village, :], temp_D2[:, action_village] = np.inf, np.inf
        temp_D1[:, action_village] = np.inf
        temp_Q[:, action_village] = -np.inf 

        vehicle_dist_lst[vehicle_i]+= reward

        vehicle_last_visited_village[vehicle_i]=villages_list[action_village]
        finished_tasks.append(villages_list[action_village])
        vehicle_visited_village[vehicle_i].append(villages_list[action_village])


    for vehicle_i in range(len(vehicles_initial_loc)):

        state_village = villages_list.index(vehicle_last_visited_village[vehicle_i])

        action_village = action_selection(state_village, episode)
        
        reward = D1[vehicle_i][state_village] 

        Q_table[state_village, action_village] += alpha * (-reward + gamma * soft_state_value_function(Q_table[action_village], temperature) - Q_table[state_village, action_village])


    plot.append(sum(vehicle_dist_lst))
    moving_avg = np.convolve(plot, np.ones(20)/20, mode='valid')
    
    if len(moving_avg)>100:

        avg_last_to_10 = np.mean(moving_avg[-1:-11:-1])
        avg_10_to_20 = np.mean(moving_avg[-11:-21:-1])

        # Check if any average is below threshold
        threshold = 1336.0
        if abs(avg_10_to_20 - avg_last_to_10)<2:
            break
    

end_time = time.time()

# Duration
duration = end_time - start_time




plot_(plot)

print()
print("Duration of for loop:", duration, "seconds")
print("Maximum time spent by a vehicle:", max(vehicle_dist_lst), "mins")
print("Total time spent by all vehicles:", sum(vehicle_dist_lst), "minssteps")


window_size =  10
moving_avg = np.convolve(plot, np.ones(window_size)/window_size, mode='valid')
plt.plot(moving_avg)
plt.show()

print("finished_tasks", vehicle_visited_village)
    

for i in vehicle_visited_village:
    nearest_depot = np.argmin(D3[villages_list.index(i[0])])
    i.insert(0,villages_list[nearest_depot])
    i.append(villages_list[nearest_depot])


print("finished_tasks", vehicle_visited_village)




# Define your routes

routes = vehicle_visited_village


#! Comment out below to visualize
# # Create a Plotly figure
# fig = go.Figure()

# # Add traces for each route with different colors
# for i, route in enumerate(routes):
#     fig.add_trace(
#         go.Scattermapbox(
#             lat=[location[0] for location in route],
#             lon=[location[1] for location in route],
#             mode='lines',
#             line=go.scattermapbox.Line(width=2, color=['red', 'blue', 'yellow', 'green'][i])
#         )
#     )

# # Add a mapbox layout with Madurai as the center location
# fig.update_layout(
#     mapbox_style="open-street-map",
#     mapbox_center_lat=9.9252,
#     mapbox_center_lon=78.1198,
#     mapbox_zoom=5
# )


# fig.show()
    