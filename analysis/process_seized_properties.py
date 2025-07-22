import argparse
import pandas as pd
import pdfplumber
import re
import json
from geopy.geocoders import GoogleV3
import time
import os

# --- CONFIGURE YOUR GOOGLE API KEY HERE ---
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY") or "YOUR_GOOGLE_API_KEY_HERE"  # Replace or set as env var

geolocator = GoogleV3(api_key=GOOGLE_API_KEY, timeout=10)

def harmonize_address(row):
    street = row.get("street", "").strip()
    housenumber = row.get("housenumber", "").strip()
    city = row.get("city", "").strip()
    address_parts = [part for part in [city, street, housenumber] if part]
    return ", ".join(address_parts)

def extract_from_pdf(pdf_path):
    records = []
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                for row in table:
                    if len(row) >= 3:
                        records.append({
                            "city": "Маріуполь",
                            "street": row[1],
                            "housenumber": row[2],
                            "type": "residential"
                        })
    df = pd.DataFrame(records)
    print(f"[DEBUG] Extracted {len(df)} residential records from PDF.")
    return df

def extract_from_xlsx(xlsx_path):
    df = pd.read_excel(xlsx_path, header=2)
    print("[DEBUG] Columns after header=2:", df.columns.tolist())
    address_col = "Адрес"
    if address_col not in df.columns:
        address_col = df.columns[2]
        print(f"[INFO] Using column '{address_col}' for address extraction.")
    df = df[df[address_col].notna()]
    def split_address(addr):
        m = re.match(r"(.+),\s*([\w\/\-]+)$", str(addr).strip())
        if m:
            return m.group(1).strip(), m.group(2).strip()
        else:
            return addr.strip(), ""
    df[["street", "housenumber"]] = df[address_col].apply(lambda x: pd.Series(split_address(x)))
    df["city"] = "Маріуполь"
    df["type"] = "commercial"
    print(f"[DEBUG] Extracted {len(df)} commercial records from XLSX after skipping 2 header rows and parsing addresses.")
    return df[["city", "street", "housenumber", "type"]]

def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            print(f"[GEOCODED] {address} -> ({location.latitude}, {location.longitude})")
            return location.latitude, location.longitude
    except Exception as e:
        print(f"[WARN] Geocoding failed for '{address}': {e}")
    return None, None

def df_to_geojson(df, out_path):
    features = []
    for _, row in df.iterrows():
        props = row.to_dict()
        features.append({
            "type": "Feature",
            "geometry": None,
            "properties": props
        })
    out = {"type": "FeatureCollection", "features": features}
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"[DEBUG] Wrote {len(features)} features to GeoJSON.")

def main():
    parser = argparse.ArgumentParser(description="Process and harmonize seized property files (PDF and XLSX).")
    parser.add_argument('--residential', required=True, help='Path to seized residential PDF')
    parser.add_argument('--commercial', required=True, help='Path to seized commercial XLSX')
    parser.add_argument('--out', required=True, help='Output GeoJSON file')
    args = parser.parse_args()

    df_res = extract_from_pdf(args.residential)
    df_com = extract_from_xlsx(args.commercial)
    df_all = pd.concat([df_res, df_com], ignore_index=True)
    df_all["address"] = df_all.apply(harmonize_address, axis=1)

    # Google geocoding for each address
    print("[INFO] Geocoding addresses, this may take a while...")
    df_all[["lat", "lon"]] = df_all["address"].apply(lambda addr: pd.Series(geocode_address(addr)))
    print("[INFO] Geocoding complete.")

    df_to_geojson(df_all, args.out)
    print(f"[INFO] Exported {len(df_all)} seized properties (residential & commercial) to {args.out}")

if __name__ == "__main__":
    main()