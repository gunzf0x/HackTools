#!/usr/bin/python3

import argparse
from argparse import RawTextHelpFormatter
from colorama import Fore, Style
import sys
from pathlib import Path
from pwn import log
import datetime
import copy
import time
import string
import signal
from itertools import combinations
import re
import random
import threading


DEFAULT_WORDLIST_DIRECTORY: str = 'wordlists'

# Ctrl+C
def sigint_handler(_, __):
    print(f'{Style.BRIGHT}{Fore.RED}[!] Ctrl+C. Exiting...{Fore.RESET}')
    sys.exit(1)


signal.signal(signal.SIGINT, sigint_handler)



def print_banner()->None:
    """
    Print a simple banner
    """
    print(f'''{Fore.BLUE}
    ____  _      __  _                             
   / __ \(_)____/ /_(_)___  ____  ____ ________  __
  / / / / / ___/ __/ / __ \/ __ \/ __ `/ ___/ / / /
 / /_/ / / /__/ /_/ / /_/ / / / / /_/ / /  / /_/ / 
/_____/_/\___/\__/_/\____/_/ /_/\__,_/_/   \__, /  
   {Fore.RED}______                __               {Fore.BLUE}/____/{Fore.RED}   
  / ____/_______  ____ _/ /_____  _____            
 / /   / ___/ _ \/ __ `/ __/ __ \/ ___/            
/ /___/ /  /  __/ /_/ / /_/ /_/ / /                
\____/_/   \___/\__,_/\__/\____/_/{Fore.RESET}                                                                                                                             
                                         {Style.BRIGHT}{Fore.CYAN}by gunzf0x{Fore.RESET}
             {Style.BRIGHT}{Fore.CYAN}(https://github.com/gunzf0x/HackTools){Fore.RESET}
    ''')

def parse_range(range_str):
    try:
        start, end = map(int, range_str.split(','))
        return list(range(start, end + 1))
    except ValueError:
        raise argparse.ArgumentTypeError("Range must be in the format 'start,end' and consist of integer values.")


def parse_arguments():
    """
    Get arguments from user
    """
    parser = argparse.ArgumentParser(prog=f'python3 dictionary_creator.py',
                                     description=f'{Style.DIM}{Fore.RED}Custom dictionary creator{Fore.RESET}',
                                     epilog=f'{Fore.YELLOW}Example usage:{Fore.RESET} python3 {sys.argv[0]} -w suspicious_words.txt',
                                     formatter_class=RawTextHelpFormatter)
    parser.add_argument('-w', '--wordlist', help=f'{Fore.BLUE}Word or list of words (file) on which the dictionary is to be based{Fore.RESET}', required=True)
    parser.add_argument('-o', '--outfile', help=f"{Fore.BLUE}Output file to save dictionary.\nIf not specified it will be saved at {Fore.RED}{DEFAULT_WORDLIST_DIRECTORY!r}{Fore.BLUE} directory\n(where {Fore.RED}{sys.argv[0]!r}{Fore.BLUE} is located){Fore.RESET}")
    parser.add_argument('-l', '--level', type=int, help='Deepness Level. Higher means more words generated.\nLvl 1 = Simple dictionary (LOW). Lvl 2 = Combined methods (MEDIUM).\nLvl 3 = Recursive and combined methods (HIGH). Default: --level=2', default=2)
    parser.add_argument('--no-numbers', help=f'{Fore.BLUE}Do not add numbers into the words created in dictionary{Fore.RESET}', action="store_true")
    parser.add_argument('--no-uppercase', help=f'{Fore.BLUE}Do not add uppercase/capital letters into the words created in dictionary{Fore.RESET}', action="store_true")
    parser.add_argument('--no-special-chars', help=f'{Fore.BLUE}Do not add special characters into the words created in dictionary{Fore.RESET}', action="store_true")
    parser.add_argument('--no-leet', help=f'{Fore.BLUE}Do not create words using l337 c0d3 l1k3 7h1s{Fore.RESET}', action="store_true")
    parser.add_argument('--no-banner', help=f'{Fore.BLUE}Do not print banner{Fore.RESET}', action="store_true")
    parser.add_argument('-b', '--arg2', help='Description of arg2\nThis is a new line for arg2 description.')
    parser.add_argument('-r', '--range', type=parse_range, help=f'Specify a range of numbers\nE.g., "0,5" will create "word0", "word1", ..., "word5"\nDefault: "0,{datetime.datetime.now().year}" (current year)',
                        default=f"0,{datetime.datetime.now().year}")
    parser.add_argument('--use-all-chars', help='Use all special chars such as "@", "&", "_", "$" and so on...\nElse, it only uses the most common one people use: ".", ",", "!", "$", "@", "&"')
    parser.add_argument('--max-special-chars-comb', type=int, help='Maximum number of special chars combination\nExample. "3" means up to "$", "$!" and "$!@" (3) combinations. Default=3\nWe do not recommend more than 4 or 5 (unless you have no option)', default=3)
    parser.add_argument('--display-all', action='store_true', help="Displays all words generated for the dictionary")
    parser.add_argument('--display-random', type=int, help='If set, displays a random number of generated words in the generated dictionary')
    # Add more arguments as needed

    args = parser.parse_args()
    return args


def check_if_file_or_string(wordlist: str)->bool:
    """
    Checks if an argument provided by the user is a file or simply a string
    """
    if Path(wordlist).is_file():
        log.info(f"{Fore.BLUE}Requested wordlist (file): {Fore.YELLOW}{Path(wordlist).resolve()}{Fore.RESET}")
        return True
    else:
        log.info(f"{Fore.BLUE}Requested word (only 1): {Fore.YELLOW}{wordlist}{Fore.RESET}")
        return False


def get_percentage(current_value: int, total_value: int)->float:
    """
    Compute percentage for an operation
    """
    return (current_value/total_value)*100


def get_words_in_file(wordlist: str, isFile: bool)-> list[str]:
    """
    Get the words from the file passed from the user (if it is not a single word)
    """
    # If it just one word, create a list with that one word
    if not isFile:
        return [wordlist]
    # If it is a file with words in every line, store every line into a list
    lines = []
    with open(Path(wordlist).resolve(), 'r') as file:
        for line in file:
        #lines.append(line.strip())
            words = line.strip().split()  # Split the line into words
            lines.extend(words)  # Extend the main list with the words
    unique_words = list(set(lines))
    log.info(f"{Fore.RED}{len(unique_words)} {Fore.BLUE}words detected in file...{Fore.RESET}")
    return unique_words


def add_numbers(wordlist: list[str], number_list: list[int], p)->list[str]:
    """
    Function to add numbers to a list
    """
    new_wordlist = []
    total_value = len(wordlist) * len(number_list)
    counter: int = 0
    for word in wordlist:
        counter += 1
        for number in number_list:
            counter += 1
            if counter % 100 == 0:
                p.status(f"{Fore.YELLOW}Adding numbers {Fore.GREEN}({counter}/{total_value} - {get_percentage(counter, total_value):.2f}%){Fore.RESET}")
            new_wordlist.append(word+str(number))
            new_wordlist.append(str(number)+word)
            new_wordlist.append(str(number)+word+str(number))
    return list(set(new_wordlist))


def pass_to_uppercase(wordlist: list[str], p)->list[str]:
    """
    Pass from lower to uppercase
    """
    variations = []
    len_wordlist: int = len(wordlist)
    for index, word in enumerate(wordlist):
        if (index + 1) % 10 == 0:
            p.status(f"Adding uppercase letters ({index+1}/{len_wordlist} - {get_percentage(index+1, len_wordlist):.2f}%)...")
        n = len(word)
        for i in range(2**n):
            temp = ""
            for j in range(n):
                if i & (1 << j):
                    temp += word[j].upper()
                else:
                    temp += word[j].lower()
            variations.append(temp)
    return variations


def pass_char_to_leet(char: str)->str:
    # If the character matches with any of these characters, return its 'leet' form
    if char.lower() == 'a':
        return '4'
    if char.lower() == 'b':
        return '8'
    if char.lower() == 'e':
        return '3'
    if char.lower() == 'g':
        return '6'
    if char.lower() == 'i':
        return '1'
    if char.lower() == 'o':
        return '0'
    if char.lower() == 's':
        return '5'
    if char.lower() == 't':
        return '7'
    # else just return its original form (unmodified)
    return char

def pass_wordlist_to_leet(wordlist: list[str], p)->list[str]:
    """
    Pass string to l337 c0d3
    """
    variations = []
    len_wordlist: int = len(wordlist)
    for index, word in enumerate(wordlist):
        if (index + 1) % 10 == 0:
            p.status(f"4dd1ng l337 c0d3 l3773r5 ({index+1}/{len_wordlist} - {get_percentage(index+1, len_wordlist):.2f}%)...")
        n = len(word)
        for i in range(2**n):
            temp = ""
            for j in range(n):
                if i & (1 << j):
                    temp += pass_char_to_leet(word[j])
                else:
                    temp += word[j]
            variations.append(temp)
    return variations

    
def add_chars(wordlist: list[str], args: argparse.Namespace, p)->list[str]:
    """
    Add special characters
    """
    if args.use_all_chars:
        special_chars = list(string.punctuation)
    else:
        special_chars = ['.', ',', '!', '$', '@', '&']
    if args.max_special_chars_comb > len(special_chars):
        log.info(f"{Fore.YELLOW}WARNING: {Fore.BLUE} changing value of '--max-special-chars-comb' from {args.max_special_chars_comb!r} to {len(special_chars)!r} (max allowed)")
        args.max_special_chars_comb = len(special_chars)

    # Create the combination of  characters
    temp_list = []
    for i in range(1, args.max_special_chars_comb+1):  #  xrange
        temp_list += list(combinations(special_chars, i))
        if i == args.max_special_chars_comb:
            break
    char_combination = [''.join(n) for n in temp_list]
    char_combination += [comb[::-1] for comb in char_combination]
    char_combination = list(set(char_combination))
    wordlist_modified: list[str] = []
    for index, word in enumerate(wordlist):
        p.status(f"{Fore.BLUE}Adding chars ({index+1}/{len(wordlist)})")
        for chars in char_combination:
            wordlist_modified.append(word+chars)
            wordlist_modified.append(chars+word)
    return list(set(wordlist_modified))


def add_stuff_to_original_wordlist(original_wordlist: list[str], args: argparse.Namespace, p)->list[str]:
    """
    Add once every algorithm to the original input. Assigned to Level 1
    """
    original_wordlist_copy = copy.deepcopy(original_wordlist)
    original_wordlist_modified: list[str] = []
    # Add numbers
    if not args.no_numbers:
        modified_wordlist_with_numbers = add_numbers(original_wordlist_copy, args.range, p)
        original_wordlist_modified += modified_wordlist_with_numbers
    if not args.no_uppercase:
        modified_wordlist_with_uppercase = pass_to_uppercase(original_wordlist_copy, p)
        original_wordlist_modified += modified_wordlist_with_uppercase
    # Return the list skipping the repeated items
    if not args.no_special_chars:
        modified_wordlist_with_special_chars: list[str] = add_chars(original_wordlist_copy, args, p)
        original_wordlist_modified += modified_wordlist_with_special_chars
    if not args.no_leet:
        modified_wordlist_leet_code: list[str] = pass_wordlist_to_leet(original_wordlist_copy, p)
        original_wordlist_modified += modified_wordlist_leet_code
    return list(set(original_wordlist_modified))


def combine_different_methods(wordlist: list[str], args: argparse.Namespace, p):
    """
    Combining different methods to create words - Level 2
    """
    original_wordlist = copy.deepcopy(wordlist)
    master_wordlist: list[str] = []
    # Add numbers - section
    if not args.no_numbers:
        original_wordlist_numbers = add_numbers(original_wordlist, args.range, p)
        master_wordlist_numbers: list[str] = []
        if not args.no_uppercase:
            master_wordlist_numbers += pass_to_uppercase(original_wordlist_numbers, p)
        if not args.no_special_chars:
            master_wordlist_numbers += add_chars(original_wordlist_numbers, args, p)
        if not args.no_leet:
            master_wordlist_numbers += pass_wordlist_to_leet(original_wordlist_numbers, p)
        master_wordlist += list(set(master_wordlist_numbers))
    # Add characters - section
    if not args.no_special_chars:
        original_wordlist_chars = add_chars(original_wordlist, args, p)
        master_wordlist_chars: list[str] = []
        if not args.no_uppercase:
            master_wordlist_chars += pass_to_uppercase(original_wordlist_chars, p)
        if not args.no_numbers:
            master_wordlist_chars += add_numbers(original_wordlist_chars, args.range, p)
        if not args.no_leet:
            master_wordlist_chars += pass_wordlist_to_leet(original_wordlist_chars, p)
        master_wordlist += list(set(master_wordlist_chars))
    return list(set(master_wordlist))


def create_dictionary(wordlist: list[str], args: argparse.Namespace)->list[str]:
    """
    Create the dictionary itself
    """
    p = log.progress(f"{Fore.CYAN}Creating dictionary{Fore.RESET}")
    # Create the main lists, a copy of the original and the one we will store all the saved words
    original_wordlist = copy.deepcopy(wordlist)
    # First, just add characters, numbers, etc to the original wordlist
    master_wordlist = [word for word in original_wordlist]
    # Let's start by adding to the original wordlist different stuff
    master_wordlist += add_stuff_to_original_wordlist(original_wordlist, args, p)
    if args.level <= 1:
        if args.level < 1:
            log.info(f"{Fore.YELLOW}WARNING: {Fore.BLUE}Fixing '--level' to '1' since the value you have passed ({args.level}) is less than the minimum allowed (1){Fore.RESET}")
            args.level = 1
        p.success(f"{Fore.GREEN}Succesfully created dictionary with {Fore.RED}{len(master_wordlist)}{Fore.GREEN} words{Fore.RESET}")
        return list(set(master_wordlist))
    if args.level == 2:
        master_wordlist_level2 = combine_different_methods(original_wordlist, args, p)
        master_wordlist += master_wordlist_level2
        p.success(f"{Fore.GREEN}Succesfully created dictionary with {Fore.RED}{len(master_wordlist)}{Fore.GREEN} words{Fore.RESET}")
        return list(set(master_wordlist_level2))+list(set(master_wordlist))


def ask_to_display()->bool:
    attempts: int = 10
    while True:
        if attempts < 0:
            return False
        response = input(f"    {Fore.YELLOW} Do you want to display ALL the generated words (it will be a mess)? ({Fore.BLUE}[Y]es{Fore.YELLOW}/{Fore.RED}[N]o{Fore.YELLOW}): {Fore.RESET}").strip()
        if re.match(r'^[Yy][Ee]?[Ss]?$', response):
            return True
        elif re.match(r'^[Nn][Oo]?$', response):
            return False
        else:
            if attempts != 0:
                print(f"\n   {Fore.RED}Invalid input. Please type 'yes' or 'no'. {Fore.YELLOW}Remaining attempts: {Fore.RED}{attempts}{Fore.RESET}")
            attempts -= 1


def display_all_generated_words(wordlist: list[str])->None:
    """
    Displays all the words from the generated dictionary
    """
    len_wordlist: int = len(wordlist)
    for index in range(0, len_wordlist):
        if index != len_wordlist-1:
            print(wordlist[index], end=', ')
        else:
            print(wordlist[index])


def display_random_words(n_displayed_words: int, wordlist: list[str])->None:
    """
    Displays random words from the generated dictionary
    """
    if n_displayed_words > len(wordlist):
        n_displayed_words = len(wordlist)
    random_selection = random.sample(wordlist, n_displayed_words)
    log.info(f"{Fore.BLUE}Displaying {Fore.RED}{n_displayed_words}{Fore.BLUE} generated random words: {Fore.RESET}")
    print("    ", end='')
    for index in range(0, len(random_selection)):
        if index != len(random_selection)-1:
            print(random_selection[index], end=" -- ")
        else:
            print(random_selection[index])


def display_info(args: argparse.Namespace, wordlist: list[str])->None:
    """
    Display info/words about the dictionary if the user wants to
    """
    if args.display_random is not None:
        display_random_words(args.display_random, wordlist)
        return
    if args.display_all:
        wantToDisplay = ask_to_display()
        if wantToDisplay:
            display_all_generated_words(wordlist)
        return
    return


def format_time(seconds):
    """
    Pass time to a minute:seconds format
    """
    # Calculate minutes and remaining seconds
    minutes = int(seconds // 60)
    remaining_seconds = seconds % 60

    # Format the time
    if minutes == 0:
        return f"{remaining_seconds:.1f} seconds"
    elif minutes == 1:
        return f"1 minute {remaining_seconds:.1f} seconds"
    else:
        return f"{minutes} minutes {remaining_seconds:.1f} seconds"


def main()->None:
    # Start timer to check script execution time
    start_time = time.time()
    # Get arguments from the user
    args = parse_arguments()
    # Print (or do not print) the banner
    if not args.no_banner:
        print_banner()
    print("Arguments provided by the user:")
    #print(args)
    # Get a list with the words to create the dictionary
    words = get_words_in_file(args.wordlist, check_if_file_or_string(args.wordlist))
    #print(words)
    words_dictionary: list[str] = create_dictionary(words, args)
    # Display some words or the whole dictionary if the user wants to
    if args.display_all or args.display_random is not None:
       display_info(args, words_dictionary)
    log.info(f"{Fore.GREEN}Execution time: {Fore.BLUE}{format_time(time.time() - start_time)}{Fore.RESET}")

    #print(words_dictionary)


if __name__ == "__main__":
    main()
    

