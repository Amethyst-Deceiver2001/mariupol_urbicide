import argparse
import json

def harmonize_address(props):
    """
    Harmonize an address from OSM properties.
    Extend this function with your normalization logic or API calls as needed.
    """
    street = props.get("addr:street", "").strip()
    housenumber = props.get("addr:housenumber", "").strip()
    city = props.get("addr:city", "").strip()
    # Compose harmonized address (customize as needed)
    address_parts = [part for part in [city, street, housenumber] if part]
    harmonized = ", ".join(address_parts)
    return harmonized

def main():
    parser = argparse.ArgumentParser(description="Harmonize and normalize Mariupol OSM data.")
    parser.add_argument('--input', required=True, help='Input file (GeoJSON)')
    parser.add_argument('--output', required=True, help='Output file (GeoJSON)')
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        data = json.load(f)
        features = data['features'] if 'features' in data else data

    harmonized_features = []
    for feat in features:
        props = feat['properties'] if 'properties' in feat else feat
        harmonized_address = harmonize_address(props)
        new_props = dict(props)
        new_props["harmonized_address"] = harmonized_address
        harmonized_features.append({
            "type": "Feature",
            "properties": new_props,
            "geometry": feat.get("geometry")  # preserve geometry if present
        })

    out_data = {
        "type": "FeatureCollection",
        "features": harmonized_features
    }
    with open(args.output, "w", encoding='utf-8') as f:
        json.dump(out_data, f, ensure_ascii=False, indent=2)
    print(f"Harmonized data written to {args.output}")

if __name__ == "__main__":
    main()