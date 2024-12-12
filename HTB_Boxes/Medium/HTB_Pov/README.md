# HTB Pov

WriteUp: [https://gunzf0x.github.io/pentesting/posts/pov/](https://gunzf0x.github.io/pentesting/posts/pov/)

`Python` script to gain a revshell to [HTB Pov](https://www.hackthebox.com/machines/pov) machine using `ViewState` command.

## Usage
```shell-session
❯ python3 request_server_exploit.py --url 'http://dev.pov.htb/portfolio/' --command '<ViewState-command>'
```
