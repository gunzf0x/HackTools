from Crypto.Cipher import AES
import argparse
from colorama import Fore, Style


def parse_arguments():
    """
    Get flags from user
    """
    parser = argparse.ArgumentParser(description=f"{Fore.RED}TeamViewer Password Decryptor.{Fore.RESET}")
    # Define flags
    parser.add_argument('-s', '--string', type=str, help='String/password to convert/encrypt', required=True)
    parser.add_argument('-o', '--outfile', type=str, help='Optional. File to write the decrypted password')
    # Parse the command line arguments
    args = parser.parse_args()
    # Return the parsed arguments
    return args


def encrypt_password(args: argparse.Namespace)->None:
    """
    Encrypt password in a TeamViewer format
    """
    # Get parameters to encrypt
    key = b"\x06\x02\x00\x00\x00\xa4\x00\x00\x52\x53\x41\x31\x00\x04\x00\x00"
    iv = b"\x01\x00\x01\x00\x67\x24\x4F\x43\x6E\x67\x62\xF2\x5E\xA8\xD7\x04"
    aes = AES.new(key, AES.MODE_CBC, IV=iv)
    # Encrypt the text
    ciphertext = aes.encrypt(args.string.ljust(32, '\x00').encode("utf-16le"))
    # Print output
    print(f"{Fore.GREEN}[+] {Fore.BLUE}Original text: {Style.BRIGHT}{Fore.RED}{args.string}{Fore.RESET}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}[+] {Fore.BLUE}Password encrypted: {Style.BRIGHT}{Fore.CYAN}{str(list(ciphertext)).replace('[','').replace(']','')}{Fore.RESET}{Style.RESET_ALL}")
    # Save the data in a file if the user passed 'outfile' option
    if args.outfile is not None:
        with open(args.outfile, 'w') as f:
            for n in list(ciphertext):
                f.write(f"{n}\n")
        print(f"{Fore.GREEN}[+] Output saved as {Fore.BLUE}{args.outfile!r}{Fore.RESET}")
    return


def main()->None:
    # Get arguments from user
    args = parse_arguments()
    # Encrypt the password passed by the user
    encrypt_password(args)


if __name__ == "__main__":
    main()
