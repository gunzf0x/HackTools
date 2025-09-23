#!/bin/bash

output="all-extensions.txt"
script="$(basename "$0")"

echo "[+] Combining all files in the current directory into a new one called '$output'"

# Empty or create the output file
> "$output"

# Loop through all files except the output and the script itself
for file in *; do
    if [[ -f "$file" && "$file" != "$output" && "$file" != "$script" ]]; then
        cat "$file" >> "$output"
    fi
done

# Remove duplicate lines (in-place safe method)
sort -u "$output" -o "$output"

echo "[+] Done."
