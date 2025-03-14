# HTB Bizness

WriteUp: [https://gunzf0x.github.io/pentesting/posts/bizness/](https://gunzf0x.github.io/pentesting/posts/bizness/)

Simple `Python` script to crack password using `SHA1` with salt in [HTB Bizness](https://www.hackthebox.com/machines/bizness) machine.

## Usage
```shell-session
❯ python3 sha1_decryptor.py --sha1 'uP0_QaVBpDWFeo8-dRzDqRwXQ2I=' --salt 'd' --wordlist '/usr/share/wordlists/rockyou.txt'
```
