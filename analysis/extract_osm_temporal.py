import argparse
import subprocess
import os
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Extract all OSM objects within Mariupol hromada from a PBF file, with optional GeoJSON export."
    )
    parser.add_argument('--input', required=True, help='Path to input .osm.pbf file')
    parser.add_argument('--output', required=True, help='Path to output file (.osm.pbf or .geojson)')
    parser.add_argument('--boundary', default='boundaries/mariupol_hromada_boundary.geojson', help='Boundary GeoJSON file')
    args = parser.parse_args()

    # Determine intermediate and final output formats
    if args.output.endswith('.osm.pbf'):
        pbf_output = args.output
        geojson_output = None
    elif args.output.endswith('.geojson'):
        pbf_output = args.output.replace('.geojson', '.osm.pbf')
        geojson_output = args.output
    else:
        print("Error: Output file must end with .osm.pbf or .geojson")
        sys.exit(1)

    # Step 1: Extract to OSM PBF (add --overwrite if file exists)
    extract_cmd = [
        "osmium", "extract",
    ]
    if os.path.exists(pbf_output):
        extract_cmd.append("--overwrite")
    extract_cmd += [
        "--polygon", args.boundary,
        "-o", pbf_output,
        args.input
    ]
    print(f"Running: {' '.join(extract_cmd)}")
    subprocess.run(extract_cmd, check=True)

    # Step 2: Convert to GeoJSON if requested (add --overwrite if file exists)
    if geojson_output:
        export_cmd = [
            "osmium", "export",
        ]
        if os.path.exists(geojson_output):
            export_cmd.append("--overwrite")
        export_cmd += [
            pbf_output,
            "-o", geojson_output
        ]
        print(f"Running: {' '.join(export_cmd)}")
        subprocess.run(export_cmd, check=True)
        print(f"GeoJSON written to {geojson_output}")

if __name__ == "__main__":
    main()