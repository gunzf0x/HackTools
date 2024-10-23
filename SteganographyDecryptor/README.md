# Stagenography Decryptor
A simple tool/`Bash` script that uses `steghide` in a loop to extract info from an image.

## Usage
```shell-session
bash ./decrypt_steg.sh <image> <password-dictionary>
```

For example:
```shell-session
bash ./decrypt_steg.sh image.jpg /usr/share/wordlists/rockyou.txt
```
