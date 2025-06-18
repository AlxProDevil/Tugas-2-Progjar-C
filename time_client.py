import socket
import sys

HOST = 'localhost'
PORT = 45000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    print(f"Connected to {HOST}:{PORT}")

    # Mengirim permintaan TIME
    request = "TIME\r\n"
    s.sendall(request.encode('utf-8'))
    print("Sent TIME, waiting answer.")
    data = s.recv(1024).decode('utf-8')
    print(f"Received: {data.strip()}")

    # Mengirim permintaan QUIT
    request = "QUIT\r\n"
    s.sendall(request.encode('utf-8'))
    
    print("Sent QUIT, closing connection.")

print("Connection closed.")