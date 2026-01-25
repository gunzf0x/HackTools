#!/usr/bin/python3
"""
Convert a binary SID encoded as a hex string (optionally prefixed with 0x)
into the textual SID (S-1-...).
"""

import sys
import argparse
import signal


# Define color dictionary
color = {
    "NC": '\033[0m',
    "RED": '\033[91m',
    "GREEN": '\033[92m',
    "YELLOW": '\033[93m',
    "BLUE": '\033[94m',
    "MAGENTA": '\033[95m',
    "CYAN": '\033[96m',
    "WHITE": '\033[97m'
}


# Define some pretty characters
STAR: str = f"{color['YELLOW']}[{color['BLUE']}*{color['YELLOW']}]{color['NC']}"
WARNING_STR: str = f"{color['RED']}[{color['YELLOW']}!{color['RED']}]{color['NC']}"


# Ctrl+C
def signal_handler(sig, frame)->None:
    print(f"\n{WARNING_STR} {color['RED']}Ctrl+C! Exiting...{color['NC']}")
    sys.exit(0)


# Capture Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def parse_arguments()->argparse.Namespace:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description=f"{color['BLUE']}Simple tool to pass a Security Identifier (SID) in hex to readable format{color['NC']}",
                                     epilog=f"""
{color['YELLOW']}Example usage:{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4{color['NC']}""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Add arguments with flags
    parser.add_argument("sid", type=str, help="SID in hex(adecimal) format to transform.")
    # Return the parsed arguments
    return parser.parse_args()


def hex_to_bytes(hexstr: str) -> bytes:
    s = hexstr.strip()
    if s.startswith("0x") or s.startswith("0X"):
        s = s[2:]
    s = s.replace(" ", "")
    return bytes.fromhex(s)


def hex_to_sid(hexstr: str, strict: bool = False) -> str:
    """
    Parse binary SID in hexstring and return the textual SID.
    strict=True will raise ValueError if the sub-authority count in header
    doesn't match the number of available sub-authorities.
    """
    b = hex_to_bytes(hexstr)
    if len(b) < 8:
        raise ValueError("Binary SID data too short (must be >= 8 bytes).")

    revision = b[0]
    sub_count = b[1]
    identifier_authority = int.from_bytes(b[2:8], "big")

    # Collect sub-authorities (each 4 bytes little-endian)
    subs = []
    offset = 8
    available = (len(b) - offset) // 4
    for _ in range(available):
        sa = int.from_bytes(b[offset:offset+4], "little")
        subs.append(sa)
        offset += 4

    if strict and available != sub_count:
        raise ValueError(f"Header says {sub_count} subauthorities, but {available} present")

    sid_parts = ["S", str(revision), str(identifier_authority)] + [str(x) for x in subs]
    sid_text = "-".join(sid_parts)
    return sid_text

if __name__ == "__main__":
    args = parse_arguments()
    try:
        sid_text = hex_to_sid(args.sid, strict=False)
        print(f"{STAR} {color['CYAN']}Hex SID: {color['GREEN']}{args.sid}{color['NC']}")
        print(f"{STAR} {color['MAGENTA']}New SID: {color['GREEN']}{sid_text}{color['NC']}")
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
