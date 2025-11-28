#!/usr/bin/env python3
import os
import base64
import argparse
import sys
import signal
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


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
STAR: str = f"{color['YELLOW']}[{color['BLUE']}+{color['YELLOW']}]{color['NC']}"
WARNING_STR: str = f"{color['RED']}[{color['YELLOW']}!{color['RED']}]{color['NC']}"


# Ctrl+C
def signal_handler(sig, frame)->None:
    print(f"\n{WARNING_STR} {color['RED']}Ctrl+C! Exiting...{color['NC']}")
    sys.exit(0)


# Capture Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def get_arguments_from_user()->argparse.Namespace:
    parser = argparse.ArgumentParser(description=f"{color['BLUE']}AES encrypt comma-separated hex bytes and output Base64-compatible ciphertext{color['NC']} by {color['RED']}gunzf0x{color['NC']}",
                                     epilog=f"""
{color['YELLOW']}Simple usage example:{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} 0xaa,0x0a,0x11{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} AA 0A 11{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} aa0a11{color['NC']}

{color['YELLOW']}Use pre-defined IV and AES Keys example:{color['NC']}
{color['GREEN']}python3 {sys.argv[0]} 0xaa,0x0a,0x11 --iv c103a602fd0a103f4186a018014413b8 --key f559f175cf94696bf9c2cf118204fe7f""",
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser = argparse.ArgumentParser(description="")
    parser.add_argument("bytes", help="Input bytes (e.g. '0xaa,0x0a,0x11')")
    parser.add_argument("--key-size", type=int, choices=[16, 24, 32], default=16,
                        help="AES key size randomly generated in bytes (16,24,32). Default: 16")
    parser.add_argument("--key", help="AES key (hex or comma-separated bytes)")
    parser.add_argument("--iv", help="IV (hex or comma-separated bytes, 16 bytes)")
    return parser.parse_args()


def check_and_generate_keys(args: argparse.Namespace):
    """
    Check if user has provided IV or AES Key. If not, randomly generate them.
    """
    # Check/generate AES key
    if args.key:
        try:
            key = parse_byte_string(args.key)
        except ValueError:
            print(f"{WARNING_STR} {color['RED']}AES key must be exactly 16, 24 or 32 bytes long{color['YELLOW']} (provided AES key has length {len(args.key)!r}) {color['NC']}")
            sys.exit(1)
    else:
        key = os.urandom(args.key_size)

    # Check/generate IV
    if args.iv:
        iv = parse_byte_string(args.iv)
        if len(iv) != 16:
            print(f"{WARNING_STR} {color['RED']}IV must be exactly 16 bytes{color['NC']}")
    else:
        iv = os.urandom(16)
    return key, iv


def parse_byte_string(byte_string: str) -> bytes:
    """
    Convert inputs like:
      "0xaa,0x0a,0x11", "aa,0a,11", "AA 0A 11", "aa0a11"
    into raw bytes
    """
    s = byte_string.strip()
    if not s:
        return b""
    # Hex string with no separators
    if "," not in s and " " not in s:
        s = s.replace("0x", "")
        if len(s) % 2 != 0:
            raise ValueError("Hex string must have even length")
        return bytes.fromhex(s)
    parts = [p.strip().lower().replace("0x", "") for p in s.replace(" ", ",").split(",") if p.strip()]
    values = [int(p, 16) for p in parts]
    if any(not (0 <= x <= 0xFF) for x in values):
        raise ValueError("Byte values must be between 0x00 and 0xFF")

    return bytes(values)


def bytes_to_0x_csv(b: bytes) -> str:
    """
    Convert b'\x0a\x0b' -> ('0x0a, 0x0b', 2)
    """
    return ", ".join(f"0x{byte:02x}" for byte in b)


def aes_encrypt_cbc(key: bytes, iv: bytes, data: bytes) -> bytes:
    """
    Encrypt bytes
    """
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()


def main()->None:
    """
    Main
    """
    # Get arguments from user / flags
    args = get_arguments_from_user()
    plaintext = parse_byte_string(args.bytes)
    # Get key and iv for encryption
    key, iv = check_and_generate_keys(args)
    # Encrypt hex bytes
    ciphertext = aes_encrypt_cbc(key, iv, plaintext)
    # Pass encrypted text to base64
    b64_ciphertext = base64.b64encode(ciphertext.hex().encode()).decode("ascii")
    # Print results
    print(f"\n\n\n{STAR}{color['GREEN']} Input (csv)        {color['NC']}:{color['BLUE']}", args.bytes, color['NC'])

    print(f"\n{STAR} {color['GREEN']}Parsed bytes (hex) {color['NC']}:{color['RED']}", plaintext.hex(), color['NC'])

    print(f"\n{STAR} {color['GREEN']}Key (hex)          {color['NC']}:{color['YELLOW']}", key.hex(), color['NC'])
    print(f"{STAR} {color['GREEN']}Key (0x csv)       {color['NC']}:{color['YELLOW']}", bytes_to_0x_csv(key), color['NC'])
    print(f"{STAR} {color['GREEN']}Key length         {color['NC']}:{color['MAGENTA']} {len(key)} bytes{color['NC']}")

    print(f"\n{STAR} {color['GREEN']}IV  (hex)          {color['NC']}:{color['YELLOW']}", iv.hex(), color['NC'])
    print(f"{STAR} {color['GREEN']}IV  (0x csv)       {color['NC']}:{color['YELLOW']}", bytes_to_0x_csv(iv), color['NC'])
    print(f"{STAR} {color['GREEN']}IV length          {color['NC']}:{color['MAGENTA']} {len(iv)} bytes{color['NC']}")

    print(f"\n{STAR} {color['GREEN']}Ciphertext (hex)   {color['NC']}:{color['CYAN']}", ciphertext.hex(), color['NC'])
    print(f"\n{STAR} {color['GREEN']}Base64 (ciphertext){color['NC']}:{color['BLUE']}", b64_ciphertext, color['NC'])

    print(f"\n{STAR}{color['CYAN']} Lengths{color['NC']}: {color['RED']}key={len(key)} iv={len(iv)} ciphertext={len(ciphertext)}{color['NC']}")


if __name__ == "__main__":
    main()
