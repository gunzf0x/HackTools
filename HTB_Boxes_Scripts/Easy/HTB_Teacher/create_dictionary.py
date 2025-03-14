#!/usr/bin/python3
import string


def create_dictionary(base_password: str, filename: str = 'potential_passwords.txt')->None:
    with open(filename, 'w') as f:
        for char in list(string.digits + string.ascii_letters + string.punctuation):
            f.write(base_password + char + "\n")
    print(f"[+] Dictionary written as {filename!r}")


def main()->None:
    base_password = 'Th4C00lTheacha'
    create_dictionary(base_password)


if __name__ == "__main__":
   main()
