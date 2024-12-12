# HTB PermX

WriteUp: [https://gunzf0x.github.io/pentesting/posts/permx/](https://gunzf0x.github.io/pentesting/posts/permx/)
Script for [HTB PermX](https://www.hackthebox.com/machines/permx) machine for `Chamilo LMS` remote code execution ([CVE-2023-4220](https://nvd.nist.gov/vuln/detail/CVE-2023-4220)).

## Usage

```shell-session
❯ python3 CVE-2023-4220.py -u http://lms.permx.htb -c '<command>'
```
