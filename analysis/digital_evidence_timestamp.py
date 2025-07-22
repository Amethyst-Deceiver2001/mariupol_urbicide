import argparse
import sys
from rfc3161ng import RemoteTimestamper, get_timestamp, check_timestamp

def main():
    parser = argparse.ArgumentParser(
        description="Creates an RFC 3161 timestamp for a file using a TSA (e.g., DigiCert)."
    )
    parser.add_argument('--input', required=True, help='Path to the input file')
    parser.add_argument('--tsa-url', default="http://timestamp.digicert.com", help='TSA server URL (RFC 3161)')
    parser.add_argument('--output', help='Path to save the .tsr (timestamp token) file')
    parser.add_argument('--verify', action='store_true', help='Immediately verify the token after creation')
    args = parser.parse_args()

    # Read input file
    try:
        with open(args.input, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file {args.input}: {e}")
        sys.exit(1)

    # Create TSA client
    try:
        tsa = RemoteTimestamper(args.tsa_url, hashname="sha256")
    except Exception as e:
        print(f"Error creating TSA client: {e}")
        sys.exit(1)

    # Request timestamp
    try:
        print("Requesting timestamp from TSA...")
        tsr = tsa.timestamp(data)
    except Exception as e:
        print(f"Error getting timestamp: {e}")
        sys.exit(1)

    # Save the .tsr file
    out_path = args.output or (args.input + ".tsr")
    try:
        with open(out_path, "wb") as f:
            f.write(tsr)
        print(f"Timestamp token saved to {out_path}")
    except Exception as e:
        print(f"Error saving file {out_path}: {e}")
        sys.exit(1)

    # Optionally verify the token
    if args.verify:
        try:
            print("Verifying timestamp token...")
            ts_info = get_timestamp(tsr)
            print(f"Timestamp: {ts_info['time']}")
            if check_timestamp(tsr, data):
                print("Timestamp token is valid for this file")
            else:
                print("Timestamp token does NOT match this file")
        except Exception as e:
            print(f"Error verifying timestamp token: {e}")
            sys.exit(1)

if __name__ == "__main__":
    main()