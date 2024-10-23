#!/bin/bash

# Example usage: bash decrypt_steg.sh image.jpg /usr/share/wordlists/rockyou.txt

# Check if the file with passwords has been provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo "[-] Usage: $0 <image> <dictionary>"
    echo "    Please provide files required."
    exit 1
fi

binary="steghide"

# Check if 'steghide' is installed
if ! command -v "$binary" &> /dev/null; then
    echo "Error: '$binary' is not installed."
    echo "Please install '$binary' to use this script."
    exit 1
fi

# Pass arguments to the script
extract_file="$1"
dictionary="$2"

# Start iterating over every line of the dictionary
while IFS= read -r password; do
  clear
  echo -ne "[+] Attempting with password: $password\r"

  # Execute 'steghide' and attempt to extract its content
  steghide extract -sf $1 -p $password 2>/dev/null

  # Check status code of the previous execution, if '0' it means the password has been found
  if [ $? -eq 0 ]; then
        echo
        echo -e "\n[+] Password found: $password"
        break
  fi
done < "$dictionary"
