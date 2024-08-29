import socket
import sys

def check_ports(host, start_port, end_port):
    open_ports = []
    for port in range(start_port, end_port + 1):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
    return open_ports

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(f"[!] Example usage: python3 {sys.argv[0]} <IP> <start-port> <end-port>")
        sys.exit(1)
    host =  sys.argv[1]
    start_port = int(sys.argv[2])
    end_port = int(sys.argv[3])

    print(f"[*] Scanning ports {start_port}-{end_port} on {host!r}...")
    open_ports = check_ports(host, start_port, end_port)

    if open_ports:
        print(f"[+] Open ports: {open_ports}")
    else:
        print("[!] No open ports found.")
