#!/usr/bin/python3

import argparse
from colorama import Fore, init
from dataclasses import dataclass
import sys
from pathlib import Path
import string


# Autoreset colors
init(autoreset=True)

# Global parameters
DEFAULT_SAVE_FILENAME: str = 'potential_users.txt'


@dataclass(kw_only=True)
class Person:
    first_name: str
    last_name: str


def parse_flags():
    """
    Get flags from the user
    """
    parser = argparse.ArgumentParser(
        description=f'{Fore.RED}Script to create users potential list{Fore.RESET}', 
        epilog="Example list: \n\nJohn Smith ---> jsmith, john.smith, johnsmith, ...\nEren Jaeger ---> ejaeger, eren.jeager, erenjaeger, ...\nGiga Chad ---> g.chad, giga.chad, gigachad, ...\n", formatter_class=argparse.RawTextHelpFormatter)
    # Add your flags here
    parser.add_argument('-l', '--list', type=str, help=f'{Fore.GREEN}List containing users in format: [First Name] [Last Name]{Fore.RESET}', required=True)
    parser.add_argument('-o', '--outfile', type=str, help='Output filename where results will be saved. Default: potential_users.txt', default="potential_users.txt")
    parser.add_argument('--add-numbers', action='store_true', help="Add numbers to the result. For example: fsmith ---> fsmith1, fsmith2, ... (up to 9)")
    # Parse the command-line arguments
    args = parser.parse_args()
    # Return the parsed arguments
    return args


def check_arguments(args:argparse.Namespace) -> None:
    """
    Check if no arguments are provided
    """
    if not any(vars(args).values()):
        print("No arguments provided. Displaying help:")
        parser = argparse.ArgumentParser(description='Script to create user potential list')
        parser.print_help()
        return


def read_file(args: argparse.Namespace) -> list[Person] | None:
    """
    Read names and lastnames from file, returning a list of persons contained within it
    """
    try:
        with open(args.list, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print(f"{Fore.RED}[-] Error. File {args.list!r} could not be found")
        sys.exit(1)
    list_Persons: list[Person] = []
    for l in lines:
        firstname = l.split()[0]
        lastname = l.split()[1]

        list_Persons.append(Person(first_name=firstname[0].upper() + firstname[1:].lower(),
                                   last_name=lastname[0].upper() + lastname[1:].lower()))
    return list_Persons
        

def get_output_file_path(path_to_analyze: str) -> str:
    """
    Check if the output file provided is an absolute path, or not. If it is an absolute path, do nothing. Else, return it as an absolute path
    """
    # Pass string to "Path" object
    path_as_Path_obj = Path(path_to_analyze)
    # Check if it is (or not) an absolute path
    if not path_as_Path_obj.is_absolute():
        path_as_Path_obj = Path.cwd() / path_as_Path_obj
    return str(path_as_Path_obj)


def create_combination(person: Person, add_number: bool):
    """
    Create different combinations for potential users and save them into a list
    """
    list_combinations: list[str] = []
    numbers = list(string.digits)
    list_combinations.append(f"{person.first_name[0].lower()}{person.last_name.lower()}")
    list_combinations.append(f"{person.first_name[:2].lower()}{person.last_name.lower()}")
    list_combinations.append(f"{person.first_name[0].lower()}.{person.last_name.lower()}")
    list_combinations.append(f"{person.first_name[:2].lower()}.{person.last_name.lower()}")
    list_combinations.append(f"{person.first_name.lower()}.{person.last_name[0].lower()}")
    list_combinations.append(f"{person.first_name.lower()}{person.last_name.lower()}")
    list_combinations.append(f"{person.first_name.lower()}.{person.last_name.lower()}")
    list_combinations.append(f"{person.first_name.lower()}")
    list_combinations.append(f"{person.last_name.lower()}")
    if add_number:
        for number in numbers:
            list_combinations.append(f"{person.first_name[0].lower()}.{person.last_name.lower()}{number}")
            list_combinations.append(f"{person.first_name[:1].lower()}.{person.last_name.lower()}{number}")
            list_combinations.append(f"{person.first_name.lower()}{person.last_name.lower()}{number}")
            list_combinations.append(f"{person.first_name.lower()}.{person.last_name.lower()}{number}")
    return list_combinations


def create_variations_and_save(potential_users: list[Person], args: argparse.Namespace) -> None:
    """
    Get the user potential list, create variations of them and add them into a list
    """
    path_to_save: str = get_output_file_path(args.outfile)
    with open(path_to_save, 'w') as f:
        f.write("Administrator\nAdmin\n") # Add Administrador and Admin users
        counter: int = 0
        for person in potential_users:
            possible_combinations = create_combination(person, args.add_numbers)
            for comb in possible_combinations:
                counter += 1
                f.write(f"{comb}\n")
            
    print(f"[+] Total number of persons: {len(potential_users)}")
    print(f"[+] Total combinations/potential users added: {counter}")
    print(f"[+] Data saved as {path_to_save!r}")
    return


def main()->None:
    # Get flags from user
    args = parse_flags()
    # Check if the user has provided correctly the arguments
    check_arguments(args)
    # Get the file containing potential users
    potential_users = read_file(args)
    # Create different combinations and save them into a file
    create_variations_and_save(potential_users, args)


if __name__ == "__main__":
    main()
