#!/usr/bin/python3
import pyperclip
import argparse
import requests
from bs4 import BeautifulSoup
from sys import exit as sys_exit


# Define color dictionary
color = {
    "RESET": '\033[0m',
    "RED": '\033[91m',
    "GREEN": '\033[92m',
    "YELLOW": '\033[93m',
    "BLUE": '\033[94m',
    "MAGENTA": '\033[95m',
    "CYAN": '\033[96m',
    "WHITE": '\033[97m'
}


# Define some pretty characters
STAR: str = f"{color['YELLOW']}[{color['BLUE']}*{color['YELLOW']}]{color['RESET']}"
WARNING_STR: str = f"{color['RED']}[{color['YELLOW']}!{color['RED']}]{color['RESET']}"


# Ctrl+C
def signal_handler(sig, frame)->None:
    """
    Ctrl+C handler
    """
    print(f"\n{WARNING_STR} {color['RED']}Ctrl+C! Exiting...{color['RESET']}")
    sys_exit(0)


def parse_arguments():
    """
    Get arguments from user
    """
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description=f"{color['GREEN']}Extract Avatars from HackTheBox machines{color['RESET']}.")
    # Add arguments with flags
    parser.add_argument("-n", "--name", type=str, help="HTB Machine name to extract avatar from.", required=True)
    parser.add_argument("-u", "--url", type=str, help="HTB base url to extract avatars from. Default: https://www.hackthebox.com/machines",
                        default='https://www.hackthebox.com/machines')
    parser.add_argument("-o", "--obsidian", action="store_true", help="Copy extracted Avatar url to display it in Obsidian notes format.")
    # Return the parsed arguments
    return parser.parse_args()


def request_avatar(args: argparse.Namespace)->None:
    """
    Extract avatar from HTB machines
    """
    # Set base url
    htb_url: str = f"{args.url}/{args.name.lower()}"
    # HTTP request to page storing the desired avatar
    print(f"{STAR} Requesting avatar to {color['GREEN']}{htb_url}{color['RESET']} url...")
    r = requests.get(htb_url)
    # Check if we were able to connect to this page
    if r.status_code != 200:
        print(f"{WARNING_STR} {color['RED']}Unable to connect to {color['YELLOW']}{htb_url}{color['RED']}. Please check connection and retry.{color['RESET']}")
        sys_exit(1)
    # Get avatar url searching in HTML elements
    print(f"{STAR} Connection successful. Attempting to extract avatar...")
    soup = BeautifulSoup(r.text, "html.parser")
    # Find the <img> tag with class "avatar" and extract the "src" attribute
    avatar_url = soup.find("img", class_="avatar")["src"]
    # Display an error message if we were not able to find avatar url
    if not avatar_url:
        print(f"{WARNING_STR} {color['RED']}Unable to find avatar url from the provided url.{color['RESET']}")
        sys_exit(1)
    # Print avatar url found
    print(f"{STAR} Avatar url found: {color['GREEN']}{avatar_url}{color['RESET']}")
    # Copy avatar url to clipboard
    try:
        if args.obsidian:
            print(f"{STAR} Copying url for Obsidian notes format to clipboard...")
            pyperclip.copy(f"![Avatar {args.name.lower()}]({avatar_url})")
        else:
            print(f"{STAR} Copying extracted url to clipboard...")
            pyperclip.copy(avatar_url)
    except Exception as e:
        print(f"{WARNING_STR}{color['RED']} Unable to copy url into clipboard. Error: {color['YELLOW']}{e}{color['RESET']}")
    print(f"{STAR} {color['CYAN']}Done.{color['RESET']}")


def main()->None:
    # Get arguments from user
    args: argparse.Namespace = parse_arguments()
    # Request avatar from HTB page
    request_avatar(args)


if __name__ == "__main__":
    main()
