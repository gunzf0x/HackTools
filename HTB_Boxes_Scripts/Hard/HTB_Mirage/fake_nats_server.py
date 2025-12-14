#!/usr/bin/python3
import socket


HOST: str = '0.0.0.0'
PORT: int = 4222


def run_fake_nats_server()->None:
    """
    Emulate a fake NATS server
    """
    print(f"[*] Fake NATS Server listening on {HOST}:{PORT}")
    # Create a socket that will handle the connection
    s = socket.socket()
    s.bind(("0.0.0.0", 4222))
    s.listen(5)
    # Start listening for a connection
    while True:
        client, addr = s.accept()
        try:
            print(f"[+] Connection from {addr}")
            # Send fake INFO (mandatory for handshake NATS)
            client.sendall(b'INFO {"server_id":"fake","version":"2.11.0","auth_required":true}\r\n')
            data = client.recv(1024)
            print("[+] Request received:")
            print(data.decode())
        except Exception as e:
            print(f"[-] Something happened:\n{e}")
        # Ensure to close the connection
        finally:
            client.close()


if __name__ == "__main__":
    run_fake_nats_server()
