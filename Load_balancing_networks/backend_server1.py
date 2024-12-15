import socket

# Define server address and port
SERVER_IP = '10.0.0.2'  # IP of backend server 1
PORT = 8081

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(5)

print(f"Server 1 running on {SERVER_IP}:{PORT}")

while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    request = client_socket.recv(1024).decode()
    print(f"Request received: {request}")
    
    # Send a basic response
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nWelcome to Server 1!"
    client_socket.sendall(response.encode())
    
    client_socket.close()
