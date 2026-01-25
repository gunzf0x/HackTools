#!/usr/bin/python3
import sys
import struct
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
    parser = argparse.ArgumentParser(description=f"{color['CYAN']}Script to pass Security Identifier (SID) to hexadecimal{color['NC']}",
                                     epilog=f"""
{color['YELLOW']}Example usage:{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} S-1-5-21-2570265163-3918697770-3667495639-1111""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    # Add arguments with flags
    parser.add_argument("sid", type=str, help="Security Identifier (SID) to pass to hexadecimal string")
    # Parse the arguments
    return parser.parse_args()


def convert_string_sid_to_binary(sid_str: str):
    parts = sid_str.split('-')
    # Check the first character is an 'S'
    if parts[0] != 'S':
        raise ValueError("Invalid SID format")
    # Divide SID into their different parts (splitted by '-')
    revision = int(parts[1])
    identifier_authority = int(parts[2])

    subauthorities = list(map(int, parts[3:]))
    subauth_count = len(subauthorities)

    binary_sid = bytearray()
    binary_sid.append(revision)
    binary_sid.append(subauth_count)

    # IdentifierAuthority is 6 bytes, big-endian
    binary_sid.extend(identifier_authority.to_bytes(6, byteorder='big'))

    # SubAuthorities are DWORDs, little-endian
    for sa in subauthorities:
        binary_sid.extend(struct.pack('<I', sa))

    return binary_sid


def main()->None:
    # Get arguments from user
    args = parse_arguments()
    # Pass SID to binary
    binary_sid = convert_string_sid_to_binary(args.sid)
    # Pass result to hexadecimal
    hex_sid = binary_sid.hex()
    # Print the result
    print(f"{STAR} {color['MAGENTA']}Given SID: {color['GREEN']}{args.sid}{color['NC']}")
    print(f"{STAR}   {color['CYAN']}Hex SID: {color['GREEN']}0x{hex_sid}{color['NC']}")


if __name__ == "__main__":
    main()
