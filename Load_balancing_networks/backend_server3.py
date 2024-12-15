import socket

# Define server address and port
SERVER_IP = '10.0.0.4'  # IP of backend server 3
PORT = 8083

# Set up the server socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((SERVER_IP, PORT))
server_socket.listen(5)

print(f"Server 3 running on {SERVER_IP}:{PORT}")

# Handle incoming client requests
while True:
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")
    
    # Receive the request from the client
    request = client_socket.recv(1024).decode()
    print(f"Request received: {request}")
    
    # Send a basic HTTP response
    response = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nWelcome to Server 3!"
    client_socket.sendall(response.encode())
    
    # Close the client connection
    client_socket.close()
