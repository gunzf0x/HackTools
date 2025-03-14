# HTB Instant

WriteUp: [https://gunzf0x.github.io/pentesting/posts/instant/](https://gunzf0x.github.io/pentesting/posts/instant/)

Simple script to run [SolarPuttyDecrypt](https://github.com/VoidSec/SolarPuttyDecrypt/) to decrypt a `PuTTY` encrypted file through bruteforce with a dictionary. Needs to be executed on a `Windows` machine (since [SolarPuttyDecrypt](https://github.com/VoidSec/SolarPuttyDecrypt/) binaries are for `Windows`).

## Usage

```shell-session
❯ C:\Users\gunzf0x\Desktop\Pentesting\SolarPuttyDecrypt> python3 .\PuTTY_decryptor.py
```
where all the needed files (`SolarPuttyDecrypt`, the encrypted `PuTTY` file and the dictionary) are all located within the same directory/folder.
