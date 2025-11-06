# Snookums - Offsec Proving Grounds
Scripts for `Snookums` machine from `Offsec Proving Grounds`. 

The following script abuses a `Remote File Inclusion` in `Simple PHP Photo Gallery` (or `SimplePHPGal`) version `0.8` and below. It starts a simple `HTTP` `Python` server on port `80` to expose `shell.php` and uses the `RFI` to remotely execute commands.

## Usage
A simple example usage is:
```shell-session
❯ python3 webshell.py 'ls -la'
```
