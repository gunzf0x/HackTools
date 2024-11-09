
#!/usr/bin/python3

# A Python3 server that accepts "POST" requests and shows the data posted on it

from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import signal
import sys
from urllib.parse import unquote


# Ctrl+C
def sigint_handler(_, __):
    print(f'\n\n[!] Ctrl+C. Exiting...')
    sys.exit(-1)


signal.signal(signal.SIGINT, sigint_handler)


parser = argparse.ArgumentParser(description=f'Simple HTTP server that accepts POST requests')
parser.add_argument('-p', '--port', type=int, default=8080, help=f'Listening port (default: 8080)')
parser.add_argument('--url-decode-output', action='store_true', help=f'URL decode the output.')
args = parser.parse_args()


# Create class that accepts POST requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"[+] Received POST data:\n", post_data)
        if args.url_decode_output:
            print(f"[+] Received POST data (url-decoded):\n", unquote(post_data))


# Run the temporal server
def run(port: int, server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"[+] Server started on port {port}...")
    httpd.serve_forever()


def main()->None:
    run(args.port)


if __name__ == '__main__':
    main()

