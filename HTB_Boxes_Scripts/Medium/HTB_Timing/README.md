# HTB Timing

`Python` script to enumerate users based on time on [HTB Timing](https://www.hackthebox.com/machines/timing) machine. Requires [xato-net-usernames](https://github.com/danielmiessler/SecLists/raw/refs/heads/master/Usernames/xato-net-10-million-usernames.txt) list and [pwntools](https://docs.pwntools.com/en/stable/about.html) installed.

## Install Pwntools
```shell-session
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade pwntools
```

## Usage
```shell-session
❯ python3 enumerate_users.py
```
