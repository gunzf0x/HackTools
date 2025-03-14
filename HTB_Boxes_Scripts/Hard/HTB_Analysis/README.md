# HTB Analysis

WriteUp: [https://gunzf0x.github.io/pentesting/posts/analysis/](https://gunzf0x.github.io/pentesting/posts/analysis/)

`Python` script for `LDAP Injection` in [HTB Analysis](https://www.hackthebox.com/machines/analysis) machine.

## Usage

Prepare all the needed libraries:
```shell-session
$ sudo apt-get update
$ sudo apt-get install python3 python3-pip python3-dev git libssl-dev libffi-dev build-essential
$ python3 -m pip install --upgrade pip
$ python3 -m pip install --upgrade pwntools
```

and run it:
```shell-session
❯ python3 exploit_ldap.py --url 'http://internal.analysis.htb/users/list.php?name'
```
