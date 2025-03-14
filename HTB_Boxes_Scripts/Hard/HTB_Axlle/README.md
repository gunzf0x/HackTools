# HTB Axlle
WriteUp: [https://gunzf0x.github.io/pentesting/posts/axlle/](https://gunzf0x.github.io/pentesting/posts/axlle/)

Simple script to build a malicious `.xll` file [HTB Axlle](https://www.hackthebox.com/machines/axlle).

## Usage
First, install `mingw`:
```shell-session
❯ sudo apt install mingw-w64 -y
```
and compile it with:
```shell-session
❯ x86_64-w64-mingw32-gcc -fPIC -luser32 -shared -o payload.xll payload.c
```
