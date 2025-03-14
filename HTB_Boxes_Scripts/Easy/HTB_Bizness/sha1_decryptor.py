#!/usr/bin/python3

import hashlib
import base64
import argparse
import sys


def percentage(number: int, total: int)->float:
    return (number/total) * 100.


def total_line_lengths(file_path: str)->int:
    total_length: int = 0
    with open(file_path, 'r', encoding='latin-1') as file:
        for line in file:
            total_length += len(line)
    return total_length


def crypt_password(salt, password):
    return hashlib.sha1((salt + password).encode('utf-8')).digest()


def crack_password(salt: str, hash: str, wordlist: str)->str|None:
    total_lines = total_line_lengths(wordlist)
    with open(wordlist, 'r', encoding='latin-1') as f:
        for index, password in enumerate(f):
            password = password.strip()
            hashed_password = base64.urlsafe_b64encode(crypt_password(salt, password)).decode('utf-8').replace('+', '.')
            print(f"[+] Attempting to crack password... ({index+1}/{total_lines} - {percentage(index+1, total_lines):.2f}%)", end="\r")
            if hashed_password == hash:
                print()
                return password
    return None


def parse_arguments()->argparse.Namespace:
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Crack SHA-1 hashed password',
                                     epilog=f'Example usage:python3 {sys.argv[0]} --salt "d" --hash "<SHA1-hash>" --wordlist "/usr/share/wordlists/rockyou.txt"',
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--sha1', type=str, help='SHA-1 hash to crack', required=True)
    parser.add_argument('--salt', type=str, help='Hash salt', required=True)
    parser.add_argument('--wordlist', type=str, help='Dictionary to attempt to crack password', required=True)
    args = parser.parse_args()
    return args


def main()->None:
    # Get arguments from user
    args = parse_arguments()
    # Attempt to crack the password
    password = crack_password(args.salt, args.sha1, args.wordlist)
    # And display the result (if there is a result)
    if password:
        print(f"[+] Password found: {password}")
        sys.exit(0)
    print("[!] Could not find a password")
    sys.exit(1)


if __name__ == "__main__":
    main()
