"""
TCP Socket Client - tallenna CSV:ksi.
"""

import socket

HOST = "172.20.241.9"
PORT = 20000
GROUPID = 15
TIEDOSTO = "socket_data.csv"

print(f"Yhdistetään {HOST}:{PORT}...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
    sock.connect((HOST, PORT))
    sock.sendall(f"{GROUPID}\n".encode('utf-8'))
    
    data = b""
    while True:
        chunk = sock.recv(4096)
        if not chunk:
            break
        data += chunk

# Tallenna CSV:nä
with open(TIEDOSTO, "w", encoding='utf-8') as f:
    f.write(data.decode('utf-8'))

rivit = len(data.split(b'\n'))
print(f"Valmis! Tallennettu {rivit} riviä tiedostoon {TIEDOSTO}")