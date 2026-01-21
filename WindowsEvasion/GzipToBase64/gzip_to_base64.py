#!/usr/bin/python3
from pathlib import Path
import argparse
import sys
import gzip
import base64


def parse_arguments()->argparse.Namespace:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Script that compress a file with GZIP and pass the result to Base64.")

    # Add arguments with flags
    parser.add_argument("filename", type=str, help="Filename to compress with GZIP and then pass it to Base64")
    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    # Parse the arguments and return them
    return parser.parse_args()


def gzip_to_base64(args: argparse.Namespace)->None:
    """
    Open a file, compress it and pass its bytes to Base64
    """
    # Open the file
    try:
        path = Path(args.filename)
        raw_bytes = path.read_bytes()
        print(f"\n[+] Opening file {path.name!r}")
    except Exception as e:
        print(f"[-] An error ocurred when opening the file:\n{e}")
        sys.exit(1)
    # Compress the file and pass it to Base64
    try:
        print("\n[+] Compressing file and passing it to Base64...")
        compressed = gzip.compress(raw_bytes)
        b64 = base64.b64encode(compressed)
    except Exception as e:
        print(f"[-] An error ocurred when coding the data:\n{e}")
        sys.exit(1)
    # Print the result
    print(f'\n[+] Encoded data in Base64:\n{b64.decode("ascii")}')
    return


def main()->None:
    # Get arguments from user
    args: argparse.Namespace = parse_arguments()
    # Compress data and pass it to Base64
    gzip_to_base64(args)


if __name__ == "__main__":
    main()
