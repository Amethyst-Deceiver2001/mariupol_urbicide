import json

# Paths to your files
cache_path = "/Users/alexeykovalev/Desktop/mariupol_project/cache/f38d80e5ba0a46f657ae03d9c9b8f447540a5210.json"
output_path = "/Users/alexeykovalev/Desktop/urbicide_project/data/raw/boundaries/mariupol_hromada_boundary.geojson"

# Load the cache file (which may be a dict or a list)
with open(cache_path, "r", encoding="utf-8") as f:
    cache = json.load(f)
    # OLD (incorrect): coordinates = cache["geojson"]["coordinates"]
    # NEW (correct):
    coordinates = None
    if isinstance(cache, dict) and "geojson" in cache:
        coordinates = cache["geojson"]["coordinates"]
    elif isinstance(cache, list):
        for item in cache:
            if "geojson" in item:
                coordinates = item["geojson"]["coordinates"]
                break
    if coordinates is None:
        raise ValueError("Could not find coordinates in cache file.")

# Find the coordinates
coordinates = None

# If cache is a dict and has 'geojson'
if isinstance(cache, dict) and "geojson" in cache:
    coordinates = cache["geojson"]["coordinates"]
# If cache is a list, search for the first object with 'geojson'
elif isinstance(cache, list):
    for item in cache:
        if "geojson" in item:
            coordinates = item["geojson"]["coordinates"]
            break

if coordinates is None:
    raise ValueError("Could not find coordinates in cache file.")

# Build the correct GeoJSON structure
geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Mariupol Urban Hromada"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": coordinates
            }
        }
    ]
}

# Write the valid GeoJSON to the correct path
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(geojson, f, ensure_ascii=False, indent=2)

print(f"✅ Valid GeoJSON written to {output_path}")