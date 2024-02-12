import argparse
import socket
import signal
import sys
import time

# Global for shutdown
not_stopped = True

# Signal handler
def signal_handler(sig, frame):
    global not_stopped
    print("Received signal {}, gracefully shutting down...".format(sig))
    not_stopped = False

def main():
    # Command-line argument parsing with custom validation
    parser = argparse.ArgumentParser(description='Server for file receiving.')
    parser.add_argument('port', type=int, 
                        help='Port number to listen on.', 
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
        server_socket.listen(10)  
        print("Server listening on port {}".format(port))
    except socket.error as msg:
        if isinstance(msg, OverflowError):
            sys.stderr.write("ERROR: Invalid port number. Port must be between 0 and 65535.\n")
        else:
            sys.stderr.write("ERROR: {}\n".format(msg)) 
        sys.exit(1)

    # Connection Handling Loop 
    while not_stopped:
        # ... (Rest of your connection handling code) 

if __name__ == '__main__':
    main()
