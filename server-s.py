import argparse
import socket
import signal
import sys
import time

# Global flag for graceful shutdown
not_stopped = True

# Signal handler
def signal_handler(sig, frame):
    global not_stopped
    print("Received signal {}, gracefully shutting down...".format(sig))
    not_stopped = False

def main():
    # Command-line argument processing
    parser = argparse.ArgumentParser(description='Server for file receiving.')
    parser.add_argument('port', type=int, help='Port number to listen on.')
    args = parser.parse_args()

    # Signal handling setup
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    # Socket initialization
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = args.port

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((HOST, PORT))
        server_socket.listen(10)  # Handle up to 10 simultaneous connections
        print("Server listening on port {}".format(PORT))
    except socket.error as msg:
        sys.stderr.write("ERROR: {}\n".format(msg))
        sys.exit(1)

    # Main connection handling loop
    while not_stopped:
        try:
            client_socket, addr = server_socket.accept()
            print("Connection established with {}".format(addr))

            # Send 'accio\r\n'
            client_socket.sendall(b'accio\r\n')

            # Receive data and calculate length with timeout
            total_bytes_received = 0
            client_socket.settimeout(10.0)  # 10-second timeout
            with client_socket:   
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        total_bytes_received += len(data)
                    except socket.timeout:
                        print("Client timed out. Connection closed.")
                        client_socket.sendall(b'ERROR\r\n')  # Send error
                        break

            print("Received {} bytes".format(total_bytes_received))

        except socket.error as msg:
            sys.stderr.write("ERROR: {}\n".format(msg))

if __name__ == "__main__":
    main()
