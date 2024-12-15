import socket
import time
import threading

def send_request(i):
    lb_ip = "10.0.0.100"  # IP of the load balancer
    lb_port = 8888  # Port on which load balancer is listening
    request = b"GET / HTTP/1.1\r\nHost: localhost\r\n\r\n"

    try:
        # Create a socket and connect to the load balancer
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((lb_ip, lb_port))
        
        # Send the GET request to the load balancer
        print(f"[Request {i}] Sending request: {request.decode('utf-8')}")
        client_socket.send(request)
        
        # Receive the response from the load balancer
        response = client_socket.recv(1024)
        print(f"[Request {i}] Received response: {response.decode('utf-8')}")
    
    except Exception as e:
        print(f"[Request {i}] Error: {e}")
    
    finally:
        # Close the socket for the current request
        client_socket.close()

def send_multiple_requests():
    threads = []
    
    # Create 100 threads to send requests in parallel
    for i in range(1, 101):
        thread = threading.Thread(target=send_request, args=(i,))
        threads.append(thread)
        thread.start()
        
        # Optional: Add a small delay to stagger the thread starts a bit
        time.sleep(0.05)
    
    # Wait for all threads to complete
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    send_multiple_requests()
