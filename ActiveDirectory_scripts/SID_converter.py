#!/usr/bin/python3
import argparse
import sys
import signal
import struct


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



def get_arguments_from_user()->argparse.Namespace:
    """
    Get arguments/flags from user.
    """
    parser = argparse.ArgumentParser(prog=f'python3 {sys.argv[0]}',
                                     description=f"{color['CYAN']}Security Identifier (SID) converter. From string to hex and viceversa.{color['NC']}")
    # Define commands
    commands = parser.add_subparsers(dest='command', help=f"{color['RED']}Available commands{color['NC']}")

    ## Define 'str2hex' command
    str2hex: str = 'str2hex' # command name
    str2hex_command = commands.add_parser(str2hex, help=f"{color['GREEN']}Convert Security Identifier (SID) to hexadecimal{color['NC']}", 
                    description=f"{color['GREEN']}Convert Security Identifier (SID) to hexadecimal{color['NC']}", 
                                           epilog=f"""
{color['YELLOW']}Example usage:{color['NC']}
{color['GREEN']}python3 {str2hex} {sys.argv[0]} S-1-5-21-2570265163-3918697770-3667495639-1111""",
                                     formatter_class=argparse.RawTextHelpFormatter)
                                     
    str2hex_command.add_argument('sid', type=str, help="Security Identifier (SID) to convert to hexadecimal string")

    ## Define 'hex2str' command
    hex2str: str = 'hex2str' # command name
    hex2str_command = commands.add_parser(hex2str, help=f"{color['BLUE']}Convert Security Identifier (SID) in hexadecimal to readable format/string{color['NC']}", 
                    description=f"{color['BLUE']}Convert Security Identifier (SID) in hexadecimal to readable format/string{color['NC']}", 
                                         epilog=f"""
{color['YELLOW']}Example usage:{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} {hex2str} 0x0105000000000005150000005B7BB0F398AA2245AD4A1CA4{color['NC']}""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    hex2str_command.add_argument('sid', type=str, help="Security Identifier (SID) in hexadecimal to convert to readable string.")
    
    return parser.parse_args()


def convert_string_sid_to_binary(sid_str: str):
    """
    Function to convert normal SID string to hexadecimal
    """
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


def main()->None:
    # Get arguments from user
    args = get_arguments_from_user()
    # Execute 'str2hex' command
    if args.command == 'str2hex':
        # Pass SID to binary
        binary_sid = convert_string_sid_to_binary(args.sid)
        # Pass result to hexadecimal
        hex_sid = binary_sid.hex()
        # Print the result
        print()
        print(f"{STAR} {color['MAGENTA']}Given SID: {color['GREEN']}{args.sid}{color['NC']}")
        print(f"{STAR}   {color['CYAN']}Hex SID: {color['GREEN']}0x{hex_sid}{color['NC']}")
    # Execute 'hex2str' command
    if args.command == 'hex2str':
        try:
            sid_text = hex_to_sid(args.sid, strict=False)
            print(f"{STAR} {color['CYAN']}Hex SID: {color['GREEN']}{args.sid}{color['NC']}")
            print(f"{STAR} {color['MAGENTA']}New SID: {color['GREEN']}{sid_text}{color['NC']}")
        except ValueError as e:
            print(f"Error: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
