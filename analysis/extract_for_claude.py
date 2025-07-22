import geopandas as gpd
import pandas as pd

# Load your Mariupol pre-war GeoJSON
gdf = gpd.read_file("mariupol.geojson")

# Prepare list for output rows
output = []

for idx, row in gdf.iterrows():
    building_type = row.get('building')
    addr_street = row.get('addr:street')
    addr_housenumber = row.get('addr:housenumber')
    apartment_count = row.get('addr:flats') or row.get('apartment') or row.get('addr:unit') or ''
    amenity = row.get('amenity')
    name = row.get('name')
    business = row.get('operator') or row.get('shop') or row.get('brand') or row.get('name') or ''
    
    # RESIDENTIAL
    if building_type in ['apartments', 'residential', 'house', 'detached']:
        output.append({
            'category': 'residential',
            'building_type': building_type,
            'street': addr_street,
            'house_number': addr_housenumber,
            'apartment_count': apartment_count,
            'amenity_type': '',
            'amenity_name': '',
            'business_name': ''
        })
    # NON-RESIDENTIAL AMENITY
    elif amenity:
        output.append({
            'category': 'non_residential_amenity',
            'building_type': building_type,
            'street': addr_street,
            'house_number': addr_housenumber,
            'apartment_count': '',
            'amenity_type': amenity,
            'amenity_name': name,
            'business_name': ''
        })
    # COMMERCIAL
    elif building_type in ['commercial', 'retail', 'office', 'industrial'] or row.get('shop'):
        output.append({
            'category': 'commercial',
            'building_type': building_type,
            'street': addr_street,
            'house_number': addr_housenumber,
            'apartment_count': '',
            'amenity_type': '',
            'amenity_name': '',
            'business_name': business
        })

# Create DataFrame and export
df = pd.DataFrame(output)
df.to_csv("mariupol_building_summary_for_claude.csv", index=False)
print(f"Exported {len(df)} rows to mariupol_building_summary_for_claude.csv")