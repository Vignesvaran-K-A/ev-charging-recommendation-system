# =====================================================
# EV SOC Prediction using Energy-based Calculation + Nearest EV Station Finder
# =====================================================

import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import matplotlib.pyplot as plt

# ------------------------------
# 1️⃣ Load Datasets
# ------------------------------
soc_file_path = input("Enter the full path to the SOC dataset CSV (only for reference if needed): ")
stations_file_path = input("Enter the full path to the Stations dataset CSV: ")

stations_df = pd.read_csv(stations_file_path)
print(f"\n✅ Stations dataset shape: {stations_df.shape}")

# Detect station name column
station_name_col = [c for c in stations_df.columns if "name" in c.lower()]
station_name_col = station_name_col[0] if station_name_col else stations_df.columns[0]

# ------------------------------
# 2️⃣ Get User EV Location
# ------------------------------
ev_lat = float(input("Enter your current EV latitude: "))
ev_lon = float(input("Enter your current EV longitude: "))

# ------------------------------
# 3️⃣ Haversine Function
# ------------------------------
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0  # km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    return R * c

# ------------------------------
# 4️⃣ Compute Distance to Each EVCS
# ------------------------------
stations_df["Distance_km"] = stations_df.apply(
    lambda row: haversine(ev_lat, ev_lon, row["Latitude"], row["Longitude"]),
    axis=1
)

nearest_stations = stations_df.nsmallest(5, "Distance_km")

# ------------------------------
# 5️⃣ Calculate SOC Needed
# ------------------------------
battery_capacity = 50   # kWh
energy_per_km = 0.18    # kWh per km

nearest_stations["Predicted_SOC_Needed"] = nearest_stations["Distance_km"].apply(
    lambda d: (d * energy_per_km / battery_capacity) * 100
)

# ------------------------------
# 6️⃣ Display Results
# ------------------------------
print("\n🔋 Predicted SOC required to reach each EVCS:\n")
print(nearest_stations[[station_name_col, "Distance_km", "Predicted_SOC_Needed"]])

# ------------------------------
# 7️⃣ Plot SOC vs Distance
# ------------------------------
plt.figure(figsize=(7,4))
plt.bar(nearest_stations[station_name_col], nearest_stations["Predicted_SOC_Needed"], color="skyblue")
plt.xlabel("EV Charging Station")
plt.ylabel("Predicted_SOC_Needed (%)")
plt.title("Predicted SOC Needed vs Distance to Nearest EVCS")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.show()