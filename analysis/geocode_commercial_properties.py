import pandas as pd
import requests
import os
import time
import geopandas as gpd
from shapely.geometry import Point

# Configuration
API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
INPUT_CSV = "data/raw/commercial_seized_cleaned.csv"
OUTPUT_CSV = "data/processed/commercial_seized_geocoded.csv"
OUTPUT_GEOJSON = "data/processed/commercial_seized_geocoded.geojson"
SUMMARY_TXT = "data/processed/commercial_seized_summary.txt"

# Load data
df = pd.read_csv(INPUT_CSV)
df["lat"] = None
df["lon"] = None

# Geocode each address
for idx, row in df.iterrows():
    address = row["address"]
    url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={API_KEY}"
    resp = requests.get(url)
    data = resp.json()
    if data["status"] == "OK":
        loc = data["results"][0]["geometry"]["location"]
        df.at[idx, "lat"] = loc["lat"]
        df.at[idx, "lon"] = loc["lon"]
    else:
        print(f"Geocoding failed for: {address} ({data['status']})")
    time.sleep(0.2)  # Be polite to the API

# Save geocoded CSV
df.to_csv(OUTPUT_CSV, index=False)

# Convert to GeoDataFrame and save as GeoJSON
gdf = gpd.GeoDataFrame(
    df.dropna(subset=["lat", "lon"]),
    geometry=[Point(xy) for xy in zip(df["lon"], df["lat"])],
    crs="EPSG:4326"
)
gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

# Write summary stats
with open(SUMMARY_TXT, "w") as f:
    f.write(f"Total entries: {len(df)}\n")
    f.write(f"Geocoded: {df[['lat','lon']].notnull().all(axis=1).sum()}\n")
    f.write(f"Missing geocode: {df[['lat','lon']].isnull().any(axis=1).sum()}\n\n")
    if "service_type" in df.columns:
        f.write("Service type counts:\n")
        f.write(df["service_type"].value_counts().to_string())
    else:
        f.write("No service_type column found.\n")

print(f"Geocoded {len(df)} commercial addresses to {OUTPUT_CSV} and {OUTPUT_GEOJSON}")