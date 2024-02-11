import socket
import sys
import signal
import time

not_stopped = True

def signal_handler(signum, frame):
    global not_stopped
    not_stopped = False
    print("Signal received, stopping server.")

# Register the signal handler for graceful shutdown
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)
signal.signal(signal.SIGQUIT, signal_handler)

def start_server(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        try:
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(10)
            print(f"Server listening on port {port}")
            
            while not_stopped:
                try:
                    client_socket, addr = server_socket.accept()
                    print(f"Connection from {addr}")
                    # Handle client connection in a separate function if needed
                except socket.timeout:
                    continue  # Continue accepting new connections
                finally:
                    if 'client_socket' in locals():
                        client_socket.close()
        except Exception as e:
            sys.stderr.write(f"ERROR: {e}\n")
        finally:
            print("Server stopped.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 server-s.py <PORT>")
        sys.exit(1)
    
    port = int(sys.argv[1])
    try:
        start_server(port)
    except ValueError:
        sys.stderr.write("ERROR: Invalid port number\n")
        sys.exit(1)

