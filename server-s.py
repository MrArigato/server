import socket
import sys
import signal
import select
import time

def handle_signal(signum, frame):
    global running
    running = False
    print("Signal received, shutting down the server.", file=sys.stderr)

# Register signal handlers
signal.signal(signal.SIGINT, handle_signal)
signal.signal(signal.SIGTERM, handle_signal)
signal.signal(signal.SIGQUIT, handle_signal)

def main(port):
    global running
    running = True
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(10)  # Listen for up to 10 connections
            server_socket.setblocking(False)
            
            print(f"Server is listening on port {port}...")
            
            while running:
                try:
                    ready_to_read, _, _ = select.select([server_socket], [], [], 1)
                    if ready_to_read:
                        client_socket, addr = server_socket.accept()
                        print(f"Connection accepted from {addr}")
                        client_socket.settimeout(10)  # Set timeout for the connection
                        
                        client_socket.sendall(b"accio\r\n")
                        
                        total_received = 0
                        while running:
                            try:
                                data = client_socket.recv(4096)
                                if not data:
                                    break
                                total_received += len(data)
                            except socket.timeout:
                                print("ERROR", file=sys.stderr)
                                break
                        
                        print(f"Connection closed. Bytes received: {total_received}")
                        client_socket.close()
                except Exception as e:
                    print(f"Error accepting connection: {e}", file=sys.stderr)
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("ERROR: Usage: python3 server-s.py <PORT>\n")
        sys.exit(1)
    
    port = None
    try:
        port = int(sys.argv[1])
    except ValueError:
        sys.stderr.write("ERROR: Port must be a number.\n")
        sys.exit(1)
    
    main(port)
