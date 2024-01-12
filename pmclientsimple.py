import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = '10.0.2.6'  # Replace with the actual server IP address
server_port = 12345  # Use the same port number as the server

client_socket.connect((server_ip, server_port))

message = "Hello from client!"
client_socket.sendall(message.encode('utf-8'))

data = client_socket.recv(1024).decode('utf-8')
print(f"Received response: {data}")

client_socket.close()
