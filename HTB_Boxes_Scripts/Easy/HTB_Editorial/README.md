# HTB Editorial
WriteUp: [https://gunzf0x.github.io/pentesting/posts/editorial/](https://gunzf0x.github.io/pentesting/posts/editorial/)

Scripts for [HTB Editorial](https://www.hackthebox.com/machines/editorial) machine.

## Server-Side Request Forgery (SSRF)
Multiprocessing `SSRF` in `Python`. This script makes multiple requests to a vulnerable url to search for internal ports open using multithreading.

### Usage
```shell-session
❯ python3 SSRF_explorer_multiprocessing.py
```

## Exposed API request endpoints
Another simple `Python` script to request exposed endpoints in the machine.

### Usage
```shell-session
❯ python3 API_request.py -e '/api/latest/metadata/messages/authors'
```
