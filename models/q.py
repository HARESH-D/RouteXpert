import numpy as np
import random

# Number of vehicles
num_vehicles = 3

# Maximum number of orders
max_no_of_orders = 8

# Function to generate unique (x, y) coordinates
def generate_unique_coordinates(num_coordinates):
    unique_coordinates = set()
    while len(unique_coordinates) < num_coordinates:
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        unique_coordinates.add((x, y))
    return list(unique_coordinates)

# Orders representing the states
orders = generate_unique_coordinates(max_no_of_orders)
print(orders)
# Initialize Q-values with zeros
Q = np.zeros((len(orders), len(orders)))

# Hyperparameters
learning_rate = 0.1
discount_factor = 0.9
epochs = 1000

# Function to calculate Manhattan distance
def manhattan_distance(order1, order2):
    return abs(order1[0] - order2[0]) + abs(order1[1] - order2[1])

# Function to initialize orders randomly without repetition
def initialize_orders():
    shuffled_orders = random.sample(orders, num_vehicles)
    return {f"vehicle_{i}": {'current_order': order, 'orders_assigned': []} for i, order in enumerate(shuffled_orders)}

# Function to find the nearest order to a given order
def find_nearest_order(order, remaining_orders):
    if remaining_orders:
        return min(remaining_orders, key=lambda o: manhattan_distance(order, o))
    else:
        return None

# Q-learning update rule
def update_q_value(state, action, reward):
    current_q_value = Q[state][action]
    max_future_q_value = np.max(Q[action, :])
    Q[state][action] = current_q_value + learning_rate * (reward + discount_factor * max_future_q_value - current_q_value)

# Function to find the optimal assignment based on the trained Q-table
def find_optimal_assignment(q_table):
    vehicle_orders = {}

    for vehicle in range(num_vehicles):
        current_order = None
        max_q_value = float('-inf')

        for state in range(len(orders)):
            # Check if the order is not already assigned
            if orders[state] not in [v['current_order'] for v in vehicle_orders.values()]:
                if q_table[state, :].max() > max_q_value:
                    max_q_value = q_table[state, :].max()
                    current_order = orders[state]

        # Assign the order with the highest Q-value to the vehicle
        vehicle_orders[f"vehicle_{vehicle}"] = {'current_order': current_order, 'orders_assigned': []}

    return vehicle_orders

# Q-learning algorithm
for epoch in range(epochs):
    remaining_orders = set(orders)
    vehicle_orders = initialize_orders()

    # Assign the 1st order to vehicles based on nearest distance
    for vehicle in range(num_vehicles):
        current_order = vehicle_orders[f"vehicle_{vehicle}"]['current_order']
        state = orders.index(current_order)
        remaining_orders.remove(current_order)
        nearest_order = find_nearest_order(current_order, remaining_orders)

        if nearest_order is not None:
            action = orders.index(nearest_order)
            reward = -manhattan_distance(current_order, nearest_order)  # Negative distance as we want to minimize it
            update_q_value(state, action, reward)
            vehicle_orders[f"vehicle_{vehicle}"]['current_order'] = nearest_order
            vehicle_orders[f"vehicle_{vehicle}"]['orders_assigned'].append(current_order)

    # Use random action selection to choose another order for each vehicle
    while remaining_orders:
        for vehicle in range(num_vehicles):
            if f"vehicle_{vehicle}" in vehicle_orders:
                current_order = vehicle_orders[f"vehicle_{vehicle}"]['current_order']
                state = orders.index(current_order)
                remaining_orders = set(list(remaining_orders)[:-1])  # Remove the last element (current_order)

                # Check if there are still unassigned orders available
                if remaining_orders:
                    # Random action selection
                    unassigned_orders = list(remaining_orders)
                    random_action = random.choice(unassigned_orders)
                    action = orders.index(random_action)

                    # Update Q-value for the random action
                    reward = -manhattan_distance(current_order, random_action)
                    update_q_value(state, action, reward)

                    # Assign the randomly chosen order to the vehicle
                    vehicle_orders[f"vehicle_{vehicle}"]['current_order'] = random_action
                    vehicle_orders[f"vehicle_{vehicle}"]['orders_assigned'].append(current_order)

# Find the most optimal assignment based on the trained Q-table
optimal_assignment = find_optimal_assignment(Q)

# Print the final Q-values
print("Final Q-values:")
# print(Q)

# Print the final assignment of each vehicle to an order
print("\nFinal assignment of each vehicle:")
for vehicle, details in vehicle_orders.items():
    print(f"{vehicle} is assigned to order {details['current_order']} and has orders assigned: {details['orders_assigned']}")

# # Print the most optimal assignment
# print("\nMost optimal assignment:")
# for vehicle, details in optimal_assignment.items():
#     print(f"{vehicle} is assigned to order {details['current_order']} and has orders assigned: {details['orders_assigned']}")
