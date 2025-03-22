# HTB Alert

WriteUp: [https://gunzf0x.github.io/pentesting/posts/alert/](https://gunzf0x.github.io/pentesting/posts/alert/)
Script for [HTB Alert](https://www.hackthebox.com/machines/alert) machine to chain `XSS` vulnerability with `LFI`.

## Usage

```shell-session
❯ python3 CVE-2023-4220.py -i <our-attacker-ip> -c '<absolute-path-file-to-read>'
```

For example:
```shell-session
❯ python3 exploit.py -i '10.10.16.3' -f '/etc/passwd'
```
