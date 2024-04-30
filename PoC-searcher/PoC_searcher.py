import argparse
import requests
import sys
import signal
from colorama import Fore
import os
from pwn import log
import re


# Define some characters
star: str =  f"{Fore.BLUE}[{Fore.GREEN}+{Fore.BLUE}]{Fore.RESET}"
warning_str: str = f"{Fore.RED}[{Fore.YELLOW}!{Fore.RED}]{Fore.RESET}"
base_script_name: str = "CVE Github Searcher" 


# Get terminal size
rows, columns = map(int, os.popen('stty size', 'r').read().split())


# Ctrl+C
def signal_handler(sig, frame):
    print(f"{warning_str} {Fore.RED}Ctrl+C. Exiting...{Fore.RESET}")
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


# Generate a whitelist with accepted commands
valid_commands_list: list[str] = ['latest', 'search', 'parameter']


# Print info about the vulnerabilities found by the API
def print_info_poc(pocs: dict)->None:
    try:
        print(f"{star} {Fore.BLUE}ID:{Fore.GREEN}", pocs["id"], Fore.RESET)
        print(f"{star} {Fore.BLUE}CVE ID:{Fore.GREEN}", pocs["cve_id"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Name:{Fore.GREEN}", pocs["name"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Owner:{Fore.GREEN}", pocs["owner"], Fore.RESET)
        print(f"{star} {Fore.BLUE}HTML URL:{Fore.GREEN}", pocs["html_url"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Description:{Fore.GREEN}", pocs["description"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Stargazers Count:{Fore.GREEN}", pocs["stargazers_count"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Vulnerability Description:{Fore.GREEN}", pocs["vuln_description"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Created At:{Fore.GREEN}", pocs["created_at"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Updated At:{Fore.GREEN}", pocs["updated_at"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Pushed At:{Fore.GREEN}", pocs["pushed_at"], Fore.RESET)
        print(f"{star} {Fore.BLUE}Inserted At:{Fore.GREEN}", pocs["inserted_at"], Fore.RESET)
        print(f"{Fore.MAGENTA}{'-'*columns}{Fore.RESET}")
    except Exception as e:
        print(f"{warning_str} {Fore.RED}An error ocurred:\n{Fore.YELLOW}{e}{Fore.RESET}")
    return

# Filter to check if a word is inside a field of a dictionary
def filter_field(word_to_filter: str, field: str):
    if field is None:
        return False
    return word_to_filter.lower() in field.lower()


# Make a request to CVEs API
def make_API_request(api_url: str, filter_word: str|None, p)->(None, dict):
    print()
    counter = 0
    p.status(f"{Fore.GREEN}Making request to {Fore.YELLOW}{api_url!r}...{Fore.RESET}")
    response = requests.get(api_url)
    if response.status_code != 200:
        p.failure(f"{Fore.RED}Request to API ({api_url})returned code {response.status_code!r}{Fore.RESET}...")
        sys.exit(1)
    # Parse the JSON response
    data = response.json()
    
    # If for some reason we have an empty list, just report it
    if len(data["pocs"]) == 0:
        p.failure(f"{Fore.RED}Data not found for requested parameters...{Fore.RESET}")
        sys.exit(1)

    # Extract data from the JSON response for "pocs" containing the keyword
    for pocs in data["pocs"][::-1]:
        # Check if the word to filter is present in any of the fields of the "pocs"
        if filter_word is not None:
            filter_id: bool = filter_field(filter_word, pocs["id"])
            filter_cve_id: bool = filter_field(filter_word, pocs["cve_id"])
            filter_name: bool = filter_field(filter_word, pocs["name"])
            filter_desc: bool = filter_field(filter_word, pocs["description"])
            filter_vuln_desc: bool = filter_field(filter_word, pocs["vuln_description"])
            filter_owner: bool = filter_field(filter_word, pocs["owner"])
            filter_html_url: bool = filter_field(filter_word, pocs["html_url"])
            final_filter = filter_id or filter_cve_id or filter_name or filter_desc or filter_vuln_desc or filter_owner or filter_html_url
            if final_filter:
                counter += 1
                print(f"{Fore.MAGENTA}{'-'*columns}{Fore.RESET}")
                print_info_poc(pocs)
        # If not, just print all the info
        else: 
            print(f"{Fore.MAGENTA}{'-'*columns}{Fore.RESET}")
            print_info_poc(pocs)
    # Check if there was no data to print
    if filter_word is not None:
        if counter == 0:
            p.failure(f"{Fore.RED}Could not find any elements with filter/word {filter_word!r}{Fore.RESET}")
            sys.exit(1)
    p.success(f"{Fore.GREEN}Data extracted from API{Fore.RESET}")
    return data


def print_command(command: str)->None:
    message: str = f" {base_script_name} | {command.upper()} "
    if len(message) >= columns:
        print(f"{Fore.GREEN}{message}{Fore.RESET}")
        return
    quantity: int = int((columns/2)) - len(message)
    print(f"{Fore.BLUE}{quantity*'='}{Fore.GREEN}{message}{Fore.BLUE}{quantity*'='}{Fore.RESET}")
    return
    

# Pass to a format 'cve-2020-9999'
def pass_to_CVE_readeable_format(vuln: str)->str:
    return vuln.strip().replace(" ", "-").lower()


# Check if the provided name is in "CVE" format
def is_cve_format(input_string):
    pattern1 = re.compile(r'\bCVE-\d{4}-\d{4,}\b', re.IGNORECASE)
    pattern2 = re.compile(r'\bCVE\s+\d{4}\s+\d{4,}\b', re.IGNORECASE)
    return bool(pattern1.match(input_string)) or bool(pattern2.match(input_string))


def run_commands(args: argparse.Namespace, base_url: str)->None:
    # Check what command to run
    if args.command == "latest":
        latest_command(args, base_url)
    elif args.command == "search":
        search_command(args, base_url)
    elif args.command == "parameter":
        parameter_command(args, base_url)
    else:
        print(f"{warning_str} Invalid command: {Fore.RED}{args.command!r}{Fore.RESET}")
        sys.exit(1)


def latest_command(args: argparse.Namespace, base_url: str)->None:
    """
    Search for latest PoCs registered
    """
    
    print_command(args.command)
    p = log.progress(f'{Fore.BLUE}Github CVE Searcher {Fore.RESET}| {Fore.RED}\'latest\'{Fore.RESET}')
    api_url: str = base_url + f'/api/v1/?limit={args.limit}'
    print(f"{star} {Fore.GREEN} Retreiving data for the latest {args.limit} PoCs uploaded to Github...{Fore.RESET}")
    data = make_API_request(api_url, args.filter, p)


def search_command(args: argparse.Namespace, base_url: str)->None:
    """
    Search for PoCs based on a CVE ID
    """
    print_command(args.command)
    if args.limit == 0:
        print(f"{warning_str} {Fore.RED}Please, set '--limit' (or '-l') parameter equal or bigger than 1 and retry...{Fore.RESET}")
        sys.exit(1)
    if not is_cve_format(args.name):
        print(f"{warning_str} {Fore.RED} Invalid name ({Fore.YELLOW}{args.name!r}{Fore.RED}). Please provide a valid CVE format like 'CVE-2020-19999' or similar...{Fore.RESET}")
    api_url: str = base_url + f"/api/v1/?cve_id={pass_to_CVE_readeable_format(args.name)}"
    if args.limit is not None:
        api_url: str = api_url + f"&limit={args.limit}"
    if args.popular:
        api_url: str = api_url + "&sort=stargazers_count"
    p = log.progress(f'{Fore.BLUE}Github CVE Searcher {Fore.RESET}| {Fore.RED}\'search\'{Fore.RESET}')
    data = make_API_request(api_url, args.filter, p)


def parameter_command(args: argparse.Namespace, base_url: str)->None:
    """
    Filter by stargazer count
    """
    if args.choice.lower() == 'popular' or args.choice.lower() == 'stargazer':
        param_search: str = 'stargazers_count'
    elif args.choice.lower() == 'updated':
        param_search: str = 'updated_at'
    elif args.choice.lower() == 'created':
        param_search: str == 'created_at'
    else:
        print(f"{warning_str} {Fore.RED}Invalid parameter choice: {args.choice!r}{Fore.RESET}")
        sys.exit(1)
    api_url: str = base_url + f'/api/v1/?sort={param_search}'
    if args.limit is not None:
        api_url: str = api_url + f'&limit={args.limit}'
    p = log.progress(f'{Fore.BLUE}Github CVE Searcher {Fore.RESET}| {Fore.RED}\'parameter\'{Fore.RESET}')
    data = make_API_request(api_url, None, p)


def valid_commands(command: str)->(str,bool):
    if command is not None:
        for c in valid_commands_list:
            if command.lower() == c.lower():
                return c.lower(), True
    return command, False


# Define a custom action class
class LimitedChoicesAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        allowed_choices = ["stargazer", "popular", "created", "updated"]
        lower_value = values.lower()
        if lower_value not in allowed_choices:
            parser.error(f"Invalid choice: {values}. Allowed choices are: {', '.join(allowed_choices)}")
        setattr(namespace, self.dest, lower_value)


def parser_arguments():
    parser = argparse.ArgumentParser(description=f"{Fore.RED}Proof of Concepts{Fore.CYAN} searcher from Github{Fore.RESET}")
    subparsers = parser.add_subparsers(title="commands", dest="command")

    # Subparser for the "latest" command
    latest_parser = subparsers.add_parser(valid_commands_list[0].lower(), help=f"{Fore.CYAN}Get the latest #N PoCs registered/uploaded at Github{Fore.RESET}")
    latest_parser.add_argument("-l", "--limit", type=int, default=10, help="Number of PoCs to retrieve")
    latest_parser.add_argument("-f", "--filter", type=str, help="Only keep results with an specific word")

    # Subparser for the "search" command
    search_parser = subparsers.add_parser(valid_commands_list[1].lower(), help=f"{Fore.CYAN}Search for CVEs PoCs uploaded to Github{Fore.RESET}")
    search_parser.add_argument("-n","--name", required=True, type=str, 
                               help=f"Search exploit by CVE ID. {Fore.YELLOW}Example: '--name CVE-2024-1086'{Fore.RESET}")
    search_parser.add_argument("-f","--filter", type=str, help="Only keep results with an specific word")
    search_parser.add_argument("-l", "--limit", type=int, help="Keep the first N results")
    search_parser.add_argument("-p","--popular",action="store_true", help="Sort by most popular repos (based on Github stargazers)")

    # Subparser for the "popular" command
    parameter_parser = subparsers.add_parser(valid_commands_list[2].lower(), help=f"{Fore.CYAN}Search PoCs by parameters such as popularity, dates, etc{Fore.RESET}")
    parameter_parser.add_argument("choice", action=LimitedChoicesAction, help="Choose from: stargazer, popular, updated, created")
    parameter_parser.add_argument("-l","--limit", help="Select the first N result for the search")

    return parser.parse_args()


def check_command(command: str, is_valid_command: bool)->None:
    if not is_valid_command:
        if command is None:
            print(f"{warning_str} You have not provided an argument.", end =' ')
        else:
            print(f"{warning_str} You have provided an invalid command ({Fore.RED}{command}{Fore.RESET}).", end = ' ')
        print("Please use the following commands: ")
        for c in valid_commands_list:
            print(f"    {Fore.YELLOW}- {Fore.BLUE}{c}{Fore.RESET}")
        print(f"     Command example: '{Fore.MAGENTA}python3 {sys.argv[0]} <command> --help{Fore.RESET}'.")
        print(f"    For example, run: '{Fore.MAGENTA}python3 {sys.argv[0]} search --help{Fore.RESET}'.")
        print(f"    You can also run: '{Fore.MAGENTA}python3 {sys.argv[0]} --help{Fore.RESET}' for more details.")
        sys.exit(1)
    return


def main()->None:
    # Base url from 'https://poc-in-github.motikan2010.net/' API
    base_url: str = 'https://poc-in-github.motikan2010.net'
    # Get arguments from user
    args: argparse.Namespace = parser_arguments()
    # Check if the passed command is valid / not an empty string. Print a help message if it is
    command, is_valid_command = valid_commands(args.command)
    check_command(command, is_valid_command)
    # Run commands
    run_commands(args, base_url)
    

if __name__ == "__main__":
    main()
