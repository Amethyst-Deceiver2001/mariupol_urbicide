import pandas as pd

IN_PATH = "data/raw/residential_seized.csv"
OUT_PATH = "data/processed/residential_harmonized.csv"

df = pd.read_csv(IN_PATH)

# Use the correct column name from your CSV
col_address = "address"

# Normalization function (same as commercial)
def norm(s):
    return str(s).lower().replace("ё", "е").replace("й", "и").replace("'", "").replace('"', '').strip()

# Parse street and house number from address
def parse_street(addr):
    # Handles "б-р Богдана Хмельницкого, д. 24, кв. 1"
    if pd.isnull(addr):
        return ""
    parts = addr.split(",")
    return norm(parts[0]) if len(parts) > 0 else ""

def parse_housenumber(addr):
    if pd.isnull(addr):
        return ""
    parts = addr.split(",")
    # Try to find part with "д." (house number)
    for part in parts:
        if "д." in part:
            return norm(part.replace("д.", ""))
    # Fallback: second part
    return norm(parts[1]) if len(parts) > 1 else ""

df["orig_address_ru"] = df[col_address]
df["street_norm"] = df[col_address].apply(parse_street)
df["housenumber_norm"] = df[col_address].apply(parse_housenumber)
df["lat"] = None
df["lon"] = None

cols_out = ["orig_address_ru", "lat", "lon", "street_norm", "housenumber_norm"]

df[cols_out].to_csv(OUT_PATH, index=False)
print(f"Harmonized residential addresses written to {OUT_PATH}")
print(df[cols_out].head())