# HTB MonitorsThree

WriteUp: [https://gunzf0x.github.io/pentesting/posts/monitorsthree/](https://gunzf0x.github.io/pentesting/posts/monitorsthree/)

Script for [HTB MonitorsThree](https://www.hackthebox.com/machines/monitorsthree) for `SQL Injection` and bypass `Duplicati` login panel.

## Usage

## SQL Injection
Only requires [PwnTools](https://docs.pwntools.com/en/stable/) library for logs/verbose.
```shell-session
❯ pip3 SQL_injection_MonitorsThree.py "http://monitorsthree.htb/forgot_password.php"
```

## Bypass Duplicati login panel
Requires `crypto-js` library. Install it with `npm install crypto-js`.
```shell-session
node Duplicati_decoder.js
```
