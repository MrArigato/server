import socket
import sys
import signal

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
        server_socket.bind(('0.0.0.0', port))
        server_socket.listen(5)  # Moderate backlog value
        print(f"Server is listening on port {port}...")

        while running:
            try:
                client_socket, addr = server_socket.accept()  # Blocking call
                print(f"Connection accepted from {addr}")

                # Handling client data
                handle_client(client_socket)

            except socket.timeout:
                continue  # Continue in case of a timeout
            except Exception as e:
                print(f"Error accepting connection: {e}")

        print("Server stopped gracefully.")

def handle_client(client_socket):
    try:
        client_socket.sendall(b"accio\r\n")
        total_received = 0

        # Receiving data loop
        while True:
            data = client_socket.recv(4096)
            if not data:
                break  # No more data, exit loop
            total_received += len(data)

        print(f"Connection closed. Bytes received: {total_received}")
    except Exception as e:
        print(f"Error during client handling: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.stderr.write("Usage: python3 server-s.py <PORT>\n")
        sys.exit(1)
    
    port = int(sys.argv[1])
    try:
        main(port)
    except Exception as e:
        sys.stderr.write(f"ERROR: {e}\n")
        sys.exit(1)
