import argparse
import sys
import asyncio
import hashlib
from pyhanko.sign.timestamps import HTTPTimeStamper
from asn1crypto import tsp, algos

async def main_async(args):
    # Read input file
    try:
        with open(args.input, "rb") as f:
            data = f.read()
    except Exception as e:
        print(f"Error reading file {args.input}: {e}")
        sys.exit(1)

    print("Requesting timestamp from TSA...")
    tsa = HTTPTimeStamper(args.tsa_url)

    # Calculate SHA256 hash
    digest = hashlib.sha256(data).digest()

    # Create TimeStampReq ASN.1 structure
    req = tsp.TimeStampReq({
        'version': 'v1',
        'message_imprint': {
            'hash_algorithm': algos.DigestAlgorithm({'algorithm': 'sha256'}),
            'hashed_message': digest
        },
        'cert_req': True
    })

    ts_response = await tsa.async_request_tsa_response(req)
    tsr = ts_response.dump()

    out_path = args.output or (args.input + ".tsr")
    try:
        with open(out_path, "wb") as f:
            f.write(tsr)
        print(f"Timestamp token saved to {out_path}")
    except Exception as e:
        print(f"Error saving file {out_path}: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Creates an RFC 3161 timestamp for a file using a TSA (e.g., DigiCert)."
    )
    parser.add_argument('--input', required=True, help='Path to the input file')
    parser.add_argument('--tsa-url', default="http://tsa.swisssign.net", help='TSA server URL (RFC 3161)')
    parser.add_argument('--output', help='Path to save the .tsr (timestamp token) file')
    args = parser.parse_args()
    asyncio.run(main_async(args))

if __name__ == "__main__":
    main()