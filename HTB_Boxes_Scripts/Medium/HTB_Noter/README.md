# HTB Noter

`Python` script to forge cookies based on an extracted secret and check -with mulltithread to speed up the process- if they are valid in a webpage for [HTB Noter](https://www.hackthebox.com/machines/noter) machine. Requires [names.txt](https://raw.githubusercontent.com/danielmiessler/SecLists/refs/heads/master/Usernames/Names/names.txt) from `SecLists`.

## Install needed libraries in a virtual environment
```shell-session
$ python3 -m venv .venv_cookies
$ source .venv_cookies/bin/activate
$ pip3 install flask-unsign pwntools
```

## Usage
```shell-session
❯ python3 test_cookie_multithread.py
```
