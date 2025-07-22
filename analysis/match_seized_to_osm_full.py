import argparse
import json

def main():
    parser = argparse.ArgumentParser(description="Match pre-war and current harmonized OSM address datasets.")
    parser.add_argument('--input-a', required=True, help='Pre-war harmonized GeoJSON')
    parser.add_argument('--input-b', required=True, help='Current harmonized GeoJSON')
    parser.add_argument('--output', required=True, help='Output CSV of matches')
    args = parser.parse_args()

    def load_addresses(path):
        with open(path, encoding='utf-8') as f:
            data = json.load(f)
            return {feat['properties']['harmonized_address'] for feat in data['features'] if 'harmonized_address' in feat['properties']}

    prewar = load_addresses(args.input_a)
    current = load_addresses(args.input_b)
    matches = prewar & current
    only_prewar = prewar - current
    only_current = current - prewar

    with open(args.output, "w", encoding='utf-8') as f:
        f.write("type,address\n")
        for addr in sorted(matches):
            f.write(f"match,{addr}\n")
        for addr in sorted(only_prewar):
            f.write(f"only_prewar,{addr}\n")
        for addr in sorted(only_current):
            f.write(f"only_current,{addr}\n")
    print(f"Match results written to {args.output}")

if __name__ == "__main__":
    main()