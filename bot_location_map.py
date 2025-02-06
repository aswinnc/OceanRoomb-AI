# bot_location.py

import random

# Initialize bot's starting location in the Indian Ocean (near Lakshadweep)
start_lat = 10.00
start_lng = 72.00
previous_lat = start_lat
previous_lng = start_lng

# Function to calculate direction
def get_direction(new_lat, new_lng):
    if new_lat > previous_lat and new_lng == previous_lng:
        return "North"
    elif new_lat < previous_lat and new_lng == previous_lng:
        return "South"
    elif new_lng > previous_lng and new_lat == previous_lat:
        return "East"
    elif new_lng < previous_lng and new_lat == previous_lat:
        return "West"
    elif new_lat > previous_lat and new_lng > previous_lng:
        return "North-East"
    elif new_lat > previous_lat and new_lng < previous_lng:
        return "North-West"
    elif new_lat < previous_lat and new_lng > previous_lng:
        return "South-East"
    else:
        return "South-West"

# Function to update the bot's location and return the current status
def get_bot_location():
    global start_lat, start_lng, previous_lat, previous_lng

    # Store the previous position before updating
    previous_lat = start_lat
    previous_lng = start_lng

    # Update the bot's position randomly to simulate movement
    start_lat += random.uniform(-0.01, 0.01)  # Random latitude movement
    start_lng += random.uniform(-0.01, 0.01)  # Random longitude movement

    # Get the direction of movement
    direction = get_direction(start_lat, start_lng)

    # Return the current location and direction
    return {
        'latitude': start_lat,
        'longitude': start_lng,
        'direction': direction
    }
