
#!/usr/bin/python3

# A Python3 server that accepts "POST" requests and shows the data posted on it

from http.server import HTTPServer, BaseHTTPRequestHandler
import argparse
import signal
import sys
from colorama import Fore
from urllib.parse import unquote

# Ctrl+C
def sigint_handler(_, __):
    print(f'\n\n{Fore.RED}[!] Ctrl+C. Exiting...{Fore.RESET}')
    sys.exit(-1)


signal.signal(signal.SIGINT, sigint_handler)


star: str = f"{Fore.BLUE}[{Fore.YELLOW}+{Fore.BLUE}]{Fore.RESET}"


parser = argparse.ArgumentParser(description=f'{Fore.CYAN}Simple HTTP server that accepts POST requests{Fore.RESET}')
parser.add_argument('-p', '--port', type=int, default=8080, help=f'{Fore.RED}Listening port (default: 8080){Fore.RESET}')
parser.add_argument('--url-decode-output', action='store_true', help=f'{Fore.RED}URL decode the output.{Fore.RESET}')
args = parser.parse_args()


# Create class that accepts POST requests
class RequestHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        print(f"{star} Received POST data:\n", post_data)
        if args.url_decode_output:
            print(f"{star} Received POST data (url-decoded):\n", unquote(post_data))


# Run the temporal server
def run(port: int, server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"{star} Server started on port {port}...")
    httpd.serve_forever()


def main()->None:
    run(args.port)


if __name__ == '__main__':
    main()

