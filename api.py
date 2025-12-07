import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "I4GdCwvjlMVlWZbVp4gEmlmEshDqJFxKwhBfEoiG"   # replace with your key

# Set your date range
start_date = datetime(2019, 1, 1)
end_date = datetime(2024, 12, 31)

# How many days per API call (NASA max is 7 but 10 works for some keys)
CHUNK_SIZE = 7

url = "https://api.nasa.gov/neo/rest/v1/feed"

all_rows = []

current_date = start_date

while current_date <= end_date:
    chunk_start = current_date
    chunk_end = min(current_date + timedelta(days=CHUNK_SIZE - 1), end_date)

    print(f"Fetching {chunk_start.date()} → {chunk_end.date()}")

    params = {
        "start_date": chunk_start.strftime("%Y-%m-%d"),
        "end_date": chunk_end.strftime("%Y-%m-%d"),
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()
        

    for date, asteroids in data["near_earth_objects"].items():
        for asteroid in asteroids:
            all_rows.append({
                "date": date,
                "id": asteroid["id"],
                "name": asteroid["name"],
                "absolute_magnitude_h": asteroid["absolute_magnitude_h"],
                "estimated_diameter_min_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_min"],
                "estimated_diameter_max_km": asteroid["estimated_diameter"]["kilometers"]["estimated_diameter_max"],
                "is_hazardous": asteroid["is_potentially_hazardous_asteroid"],
                "miss_distance_km": asteroid["close_approach_data"][0]["miss_distance"]["kilometers"],
                "relative_velocity_kph": asteroid["close_approach_data"][0]["relative_velocity"]["kilometers_per_hour"]
            })

    current_date += timedelta(days=CHUNK_SIZE)

# Create DataFrame
df = pd.DataFrame(all_rows)

# Save to CSV
df.to_csv("neo_data.csv", index=False)
