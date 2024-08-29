
#!/bin/bash

# Check if the correct number of arguments is provided
if [ "$#" -ne 4 ]; then
  echo "Usage: $0 <IP_ADDRESS> <START_PORT> <END_PORT> <THREADS>"
  exit 1
fi

IP_ADDRESS=$1
START_PORT=$2
END_PORT=$3
THREADS=$4

# Function to scan a single port
scan_port() {
  PORT=$1
  if (echo > /dev/tcp/$IP_ADDRESS/$PORT) >/dev/null 2>&1; then
    echo "[+] Port $PORT is open"
  fi
}

# Export the function for parallel execution
export -f scan_port
export IP_ADDRESS

# Scan ports in parallel
for PORT in $(seq $START_PORT $END_PORT); do
  echo $PORT
done | xargs -P $THREADS -I {} bash -c 'scan_port "$@"' _ {}

