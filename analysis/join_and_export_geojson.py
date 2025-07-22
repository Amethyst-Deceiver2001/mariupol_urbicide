import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# File paths
COMM_PATH = "data/processed/commercial_harmonized.csv"
RES_PATH = "data/processed/seized_properties_combined.csv"
OUT_GEOJSON = "data/processed/seized_properties_combined.geojson"
OUT_CSV = "data/processed/seized_properties_combined.csv"

def norm(s):
    return str(s).lower().replace("ё", "е").replace("й", "и").replace("'", "").replace('"', '').strip()

# --- Commercial ---
df_com = pd.read_csv(COMM_PATH)
if "street_norm" not in df_com.columns:
    df_com["street_norm"] = df_com["orig_address_ru"].apply(lambda x: norm(x.split(",")[0]) if pd.notnull(x) else "")
    df_com["housenumber_norm"] = df_com["orig_address_ru"].apply(lambda x: norm(x.split(",")[1]) if (pd.notnull(x) and "," in x) else "")
df_com["source"] = "commercial"

# --- Residential ---
df_res = pd.read_csv(RES_PATH)
df_res = df_res[df_res["type"] == "residential"].copy()
df_res["street_norm"] = df_res["street"].apply(norm)
df_res["housenumber_norm"] = df_res["housenumber"].apply(norm)
df_res["source"] = "residential"
df_res["orig_address_ru"] = df_res["street"]

# --- Harmonize columns ---
com_cols = ["orig_address_ru", "address_ua", "lat", "lon", "street_norm", "housenumber_norm", "source"]
res_cols = ["orig_address_ru", "address", "lat", "lon", "street_norm", "housenumber_norm", "source"]

# Ensure residential has 'address_ua' for compatibility
df_res.rename(columns={"address": "address_ua"}, inplace=True)

df_com_out = df_com[com_cols]
df_res_out = df_res[com_cols]

# --- Combine ---
df_all = pd.concat([df_com_out, df_res_out], ignore_index=True)
df_all = df_all[df_all["lat"].notnull() & df_all["lon"].notnull()]

# --- Export to CSV ---
df_all.to_csv(OUT_CSV, index=False)
print(f"Combined CSV written to {OUT_CSV}")

# --- Export to GeoJSON ---
gdf = gpd.GeoDataFrame(
    df_all,
    geometry=[Point(float(x), float(y)) for x, y in zip(df_all["lon"], df_all["lat"])],
    crs="EPSG:4326"
)
gdf.to_file(OUT_GEOJSON, driver="GeoJSON")
print(f"Combined GeoJSON written to {OUT_GEOJSON}")