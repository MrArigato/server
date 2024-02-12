import argparse
import socket
import signal
import sys
import time

# Global flag for graceful shutdown
not_stopped = True

# Custom signal handler
def signal_handler(sig, frame):
    global not_stopped
    print("Received signal {}, gracefully shutting down...".format(sig))
    not_stopped = False

def main():
    # Command-line argument processing with port validation
    parser = argparse.ArgumentParser(description='Server for file receiving.')
    parser.add_argument('port', type=int, help='Port number to listen on.', 
                        choices=range(0, 65536))
    args = parser.parse_args()

    # Setup signal handling
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGQUIT, signal_handler)

    # Socket initialization
    host = '0.0.0.0'  # Listen on all interfaces
    port = args.port

    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(10)  # Allow up to 10 simultaneous connections
        print("Server listening on port {}".format(port))
    except socket.error as msg:
        if isinstance(msg, OverflowError):
            sys.stderr.write("ERROR: Invalid port number. Port must be between 0 and 65535.\n")
        else:
            sys.stderr.write("ERROR: {}\n".format(msg))
        sys.exit(1)

    # Connection handling loop
    while not_stopped:
        try:
            client_socket, addr = server_socket.accept()
            print("Connection established with {}".format(addr))

            # Send 'accio\r\n'
            client_socket.sendall(b'accio\r\n')

            # Data reception (with a 10-second inactivity  timeout)
            total_bytes_received = 0
            client_socket.settimeout(10.0)
            with client_socket:
                while True:
                    try:
                        data = client_socket.recv(1024)
                        if not data:
                            break
                        total_bytes_received += len(data)
                    except socket.timeout:
                        print("Client timed out. Connection closed")
                        client_socket.sendall(b'ERROR\r\n')
                        break

            print("Received {} bytes".format(total_bytes_received))

        except socket.error as msg:
            sys.stderr.write("ERROR: {}\n".format(msg))

if __name__ == '__main__':
    main()
