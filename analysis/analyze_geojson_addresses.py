import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Analyze harmonized Mariupol OSM addresses.")
    parser.add_argument('--input', required=True, help='Input harmonized GeoJSON file')
    parser.add_argument('--output', required=True, help='Output analysis CSV file')
    args = parser.parse_args()

    with open(args.input, encoding='utf-8') as f:
        data = json.load(f)
        features = data['features']

    unique_addresses = set()
    for feat in features:
        addr = feat['properties'].get('harmonized_address')
        if addr:
            unique_addresses.add(addr)

    with open(args.output, "w", encoding='utf-8') as f:
        f.write("unique_address_count\n")
        f.write(f"{len(unique_addresses)}\n")
    print(f"Analysis written to {args.output}")

if __name__ == "__main__":
    main()