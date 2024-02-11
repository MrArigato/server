import socket
import sys
import signal
import time

# Global variable to control the server's running state.
not_stopped = True

def signal_handler(signum, frame):
    global not_stopped
    not_stopped = False

# Register signal handlers for graceful termination.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)

def start_server(port):
    # Create a socket object using IPv4 and TCP protocol.
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    try:
        # Bind the socket to all interfaces and the specified port.
        server_socket.bind(('0.0.0.0', port))
        # Listen for connections, with a specified backlog.
        server_socket.listen(10)
    except Exception as e:
        sys.stderr.write("ERROR: {}\n".format(e))
        sys.exit(1)
    
    print(f"Server is listening on port {port}...")
    
    while not_stopped:
        try:
            # Accept a connection.
            client_socket, addr = server_socket.accept()
            print(f"Connection from {addr}")
            client_socket.settimeout(10)  # Set timeout for client operations.
            
            # Send a greeting message to the client.
            client_socket.sendall(b"accio\r\n")
            
            received_data_length = 0
            while True:
                try:
                    # Receive data in chunks.
                    data = client_socket.recv(4096)
                    if not data:
                        break  # Break if no data is received.
                    received_data_length += len(data)
                except socket.timeout:
                    client_socket.sendall(b"ERROR")
                    break
            
            # Print the amount of received data after connection is terminated.
            print(f"Connection closed. Bytes received: {received_data_length}")
            
            client_socket.close()
        except KeyboardInterrupt:
            break
    
    # Close the server socket before exiting.
    server_socket.close()
    print("Server stopped.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server-s.py <PORT>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    start_server(port)
