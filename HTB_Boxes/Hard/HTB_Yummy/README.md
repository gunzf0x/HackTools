# HTB Yummy

WriteUp: [https://gunzf0x.github.io/pentesting/posts/yummy/](https://gunzf0x.github.io/pentesting/posts/yummy/)

`Python` scripts to abuse `Local File Inclusion` (`LFI`) at [HTB Yummy](https://www.hackthebox.com/machines/yummy) to read system files.

---

## Local File Inclusion

### Usage

To use credentials with a user whose email is `gunzf0x@gunzf0x.htb`, username `gunzf0x`, password `gunzf0x123!$` and we want to read `/etc/passwd` through `LFI`, we can run:
```shell-session
❯ python3 lfi.py -e 'gunzf0x@gunzf0x.htb' -u 'gunzf0x' -p 'gunzf0x123!$' -f '/etc/passwd'
```
If we, additionally, want to also _create_ the user account at `yummy.htb` site, we can also use `--create-account` flag:
```shell-session
❯ python3 lfi.py -e 'gunzf0x@gunzf0x.htb' -u 'gunzf0x' -p 'gunzf0x123!$' -f '/etc/passwd' --create-account
```

---

## Modify JWT using RSA256 algorithm
To modify the `Jason Web Token` obtained from a user using `RSA256` algorithm we can run, for example:
### Usage
```shell-session
❯ python3 modify_original_token.py -t 'eyJhbGc<SNIP>94gzOkXs'
```
Where `eyJhbGc<SNIP>94gzOkXs` is an original `JWT` extracted from our user at `yummy.htb` webpage.
