# TeamViewerPasswordDecryptor

Password decryptor for TeamViewer

## Usage
If we manage to get, for example `SecurityPasswordAES` properties in a system, it might look like a list of integer numbers. Save that list into a file (for example, `example.txt`), run this script and get the decrypted password

```shell-session
python3 decrypt_password_teamviewer.py -l example.txt
```


### Password encryptor
Just for fun, if you would like to see how a password (or simply a string) would look encrypted in this way I added an `encryptor_password_teamviewer.py`. Passing an argument to `-o / --outfile` flag saves the output into a file.
```shell-session
python3 encryptor_password_teamviewer.py -s 'P455w0rd!$!'
```
will return
```shell-session
[+] Original text: P455w0rd!$!
[+] Password encrypted: 119, 79, 6, 105, 195, 240, 210, 192, 94, 103, 152, 28, 44, 137, 129, 227, 254, 202, 227, 144, 205, 229, 29, 205, 195, 37, 11, 95, 55, 108, 51, 175, 19, 94, 115, 183, 138, 87, 4, 42, 121, 238, 13, 112, 163, 125, 225, 207, 19, 51, 222, 75, 234, 70, 8, 218, 197, 187, 82, 241, 191, 86, 9, 13
```
