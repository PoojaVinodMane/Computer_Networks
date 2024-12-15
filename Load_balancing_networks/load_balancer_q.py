import socket
import random
import time
import threading
import queue

# Backend server configurations
backend_servers = [
    ("10.0.0.2", 8081),
    ("10.0.0.3", 8082),
    ("10.0.0.4", 8083),
]

# Global variables for metrics
overall_response_time = 0
overall_latency = 0
total_data_transferred = 0
overall_throughput = 0
total_sessions = 0

# Initialize metrics for each session
session_metrics = {
    'response_time': 0,
    'latency': 0,
    'requests': 0,
    'data_transferred': 0
}

# For round-robin load balancing
current_server = 0  # Tracks the current server index in round-robin

# List to store per-request metrics for calculating averages
request_metrics = []
server_queues = {i: queue.Queue() for i in range(len(backend_servers))}

# Server load and response time tracking
SERVER_LOAD = [0] * len(backend_servers)
SERVER_RESPONSE_TIMES = [0] * len(backend_servers)
LOCK = threading.Lock()

def is_server_available(ip, port):
    """Check server availability."""
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.settimeout(2)
        server_socket.connect((ip, port))
        server_socket.close()
        return True
    except (socket.timeout, socket.error):
        return False

def forward_request(client_socket, server_ip, server_port, server_index):
    global overall_response_time, overall_latency, overall_throughput, total_sessions, total_data_transferred
    """Forward request to backend server and measure response time."""
    try:
        start_time = time.time()
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((server_ip, server_port))

        # Receive client request
        request = client_socket.recv(1024)
        print(f"Forwarding request to {server_ip}:{server_port} -> {request.decode('utf-8')}")
        server_socket.send(request)

        # Receive and forward response
        response = server_socket.recv(1024)
        session_metrics['data_transferred'] += len(response)
        first_byte_time = time.time()
        client_socket.send(response)

        # Measure response time
        response_time = time.time() - start_time
        latency = first_byte_time - start_time
        update_response_time(server_index, response_time)
        # Update session metrics
        session_metrics['response_time'] += response_time
        session_metrics['latency'] += latency
        session_metrics['requests'] += 1

        # Store the metrics for each request
        request_metrics.append({
            'response_time': response_time,
            'latency': latency,
            'throughput': len(response)
        })

        # Update overall metrics (including total data transferred and response time)
        with LOCK:
            total_sessions += 1
            total_data_transferred += len(response)
            overall_response_time = (overall_response_time * (total_sessions - 1) + response_time) / total_sessions
            overall_latency = (overall_latency * (total_sessions - 1) + latency) / total_sessions

        # Calculate throughput as total data transferred divided by total response time
        if overall_response_time > 0:  # Prevent division by zero
            throughput = total_data_transferred / overall_response_time
        else:
            throughput = 0

        print(f"\n--- Overall Metrics for sessions {total_sessions}")
        print(f"Overall Average Latency: {overall_latency:.4f} seconds")
        print(f"Overall Average Response Time: {overall_response_time:.4f} seconds")
        print(f"Overall Average Throughput: {throughput:.2f} bytes/second\n")

    except Exception as e:
        print(f"Error communicating with server {server_ip}:{server_port}: {e}")
    finally:
        server_socket.close()
        client_socket.close()

def update_response_time(server_index, response_time):
    """Update the average response time for the server."""
    with LOCK:
        SERVER_RESPONSE_TIMES[server_index] = (
            (SERVER_RESPONSE_TIMES[server_index] + response_time) / 2
        )

def process_queue(server_index):
    """Process requests from the server's queue."""
    server_ip, server_port = backend_servers[server_index]
    while True:
        client_socket = server_queues[server_index].get()  # Wait for a request
        if is_server_available(server_ip, server_port):
            with LOCK:
                SERVER_LOAD[server_index] += 1
            try:
                forward_request(client_socket, server_ip, server_port, server_index)
            finally:
                with LOCK:
                    SERVER_LOAD[server_index] -= 1
        else:
            print(f"Server {server_ip}:{server_port} is unavailable. Retrying...")
            server_queues[server_index].put(client_socket)  # Requeue the request
        server_queues[server_index].task_done()

def find_best_server():
    """Find the server with the least average response time."""
    with LOCK:
        min_response_time = min(SERVER_RESPONSE_TIMES)
        best_server_index = SERVER_RESPONSE_TIMES.index(min_response_time)
    return best_server_index

def handle_client(client_socket, lb_method):
    """Handle client request and forward to appropriate backend server."""
    global current_server
    if lb_method == "round_robin":
        with LOCK:
            server_index = current_server
            current_server = (current_server + 1) % len(backend_servers)
    elif lb_method == "random":
        server_index = random.randint(0, len(backend_servers) - 1)
    elif lb_method == "least_response_time":
        server_index = find_best_server()
    else:
        print("Invalid load balancing method")
        client_socket.close()
        return

    server_queues[server_index].put(client_socket)  # Enqueue the request

def load_balancer(lb_ip, lb_port, lb_method):
    lb_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lb_socket.bind((lb_ip, lb_port))
    lb_socket.listen(5)
    print(f"{lb_method.capitalize()} Load Balancer running on {lb_ip}:{lb_port}...")

    # Start server queue processing threads
    for i in range(len(backend_servers)):
        threading.Thread(target=process_queue, args=(i,), daemon=True).start()

    while True:
        client_socket, client_address = lb_socket.accept()
        print(f"Connection from {client_address}")
        threading.Thread(target=handle_client, args=(client_socket, lb_method)).start()

def main():
    lb_ip = "10.0.0.100"
    lb_port = 8888

    print("Select Load Balancing Algorithm:")
    print("1. Round Robin")
    print("2. Random")
    print("3. Least Response Time")

    choice = input("Enter the number of the algorithm you want to use: ")
    methods = {"1": "round_robin", "2": "random", "3": "least_response_time"}
    lb_method = methods.get(choice)

    if lb_method:
        load_balancer(lb_ip, lb_port, lb_method)
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()