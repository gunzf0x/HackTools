# Stagenography Decryptor
A simple tool/`Bash` script that uses `steghide` in a loop to extract info from an image bruteforcing it.

## Usage
```shell-session
bash ./decrypt_steg_bruteforce.sh <image> <password-dictionary>
```

For example:
```shell-session
bash ./decrypt_steg_bruteforce.sh image.jpg /usr/share/wordlists/rockyou.txt
```
