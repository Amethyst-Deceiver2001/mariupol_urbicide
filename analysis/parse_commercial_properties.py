import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import re

INPUT_CSV = "data/processed/seized_properties_combined.csv"
OUTPUT_CSV = "data/processed/commercial_clean.csv"
OUTPUT_GEOJSON = "data/processed/commercial_clean.geojson"

# Load combined data
df = pd.read_csv(INPUT_CSV)

# Filter for commercial entries (adjust if your type column uses different values)
commercial_mask = df["type"].str.lower().str.contains("commercial|нежилое")
df_commercial = df[commercial_mask].copy()

# If you have a column with service info (e.g., "магазин 'Марат'"), parse it:
def parse_service_info(address):
    # Example: extract type and name from address string
    # Adjust regex as needed for your data format
    m = re.search(r"(магазин|павильон|парикмахерская|кафе|аптека|банк|отель|ресторан|бар|салон|продукты|цветы|склад|офис|школа|детсад|университет|библиотека|театр|кинотеатр|спортзал|unknown)[\s\"']*([^\"]+)?", address, re.IGNORECASE)
    if m:
        return pd.Series([m.group(1).lower(), (m.group(2) or "").strip()])
    return pd.Series(["unknown", ""])

df_commercial[["service_type", "service_name"]] = df_commercial["address"].apply(parse_service_info)

# Keep only relevant columns, add geometry for GeoJSON
keep_cols = ["city", "street", "housenumber", "type", "service_type", "service_name", "address", "lat", "lon"]
df_commercial = df_commercial[keep_cols]

# Drop rows without coordinates
df_commercial = df_commercial.dropna(subset=["lat", "lon"])

# Save cleaned commercial CSV
df_commercial.to_csv(OUTPUT_CSV, index=False)

# Save as GeoJSON
gdf = gpd.GeoDataFrame(
    df_commercial,
    geometry=[Point(xy) for xy in zip(df_commercial["lon"], df_commercial["lat"])],
    crs="EPSG:4326"
)
gdf.to_file(OUTPUT_GEOJSON, driver="GeoJSON")

print(f"Exported {len(df_commercial)} commercial properties to {OUTPUT_CSV} and {OUTPUT_GEOJSON}")