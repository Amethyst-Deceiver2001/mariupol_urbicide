# Makefile for Mariupol Property Analysis

# Extract addresses from PDF to CSV
extract-residential:
	python analysis/extract_residential_addresses.py

# Geocode addresses and export minimal CSV/GeoJSON
geocode-residential:
	python analysis/geocode_residential_properties.py

# Process UNOSAT damage data
process-unosat:
	python analysis/process_unosat_damage.py

# Download and extract building footprints
download-footprints:
	python analysis/download_ukraine_building_footprints.py

# Filter points in a GeoJSON (example utility)
filter-points:
	python analysis/filter_points_geojson.py

# Convert GeoJSON to CSV (example utility)
geojson-to-csv:
	python analysis/geojson_to_csv.py

# Run all main steps (customize as needed)
all: extract-residential geocode-residential process-unosat