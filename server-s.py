import socket
import sys
import signal
import select

# Flag to control the server's main loop
running = True

def handle_signal(signum, frame):
    global running
    running = False
    print("Signal received, shutting down the server.")

# Register signal handlers for graceful termination
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGQUIT, handle_signal)

def main(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(10)  # Listen for connections, support up to 10 simultaneous connections
            server_socket.setblocking(False)  # Set socket to non-blocking mode
            
            print(f"Server is listening on port {port}...")
            
            while running:
                ready_to_read, _, _ = select.select([server_socket], [], [], 1)
                if ready_to_read:
                    client_socket, addr = server_socket.accept()
                    print(f"Connection accepted from {addr}")
                    client_socket.sendall(b"accio\r\n")
                    
                    total_received = 0
                    while running:
                        try:
                            data = client_socket.recv(4096)
                            if not data:
                                break
                            total_received += len(data)
                        except socket.error:
                            break
                    
                    print(f"Connection closed. Bytes received: {total_received}")
                    client_socket.close()
        except Exception as e:
            sys.stderr.write(f"ERROR: {e}\n")
            sys.exit(1)
        finally:
            print("Server stopped gracefully.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 server-s.py <PORT>\n")
        sys.exit(1)
    
    port = int(sys.argv[1])
    main(port)
