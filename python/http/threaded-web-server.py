import socket
from socket import socket as Socket
import argparse
import sys
import threading

def listen(connection_socket, addr):
    request = connection_socket.recv(1024).decode('ascii')
    reply = http_handle(request)
    connection_socket.send(reply.encode('ascii'))
    connection_socket.close()




def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', '-p', default=2080, type=int, help='Port to use')
    args = parser.parse_args()

    # Create the server socket (to handle tcp requests using ipv4), make sure
    # it is always closed by using with statement.
    with Socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:

        # The socket stays connected even after this script ends. So in order
        # to allow the immediate reuse of the socket (so that we can kill and
        # re-run the server while debugging) we set the following option. This
        # is potentially dangerous in real code: in rare cases you may get junk
        # data arriving at the socket.
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        server_socket.bind(('127.0.0.1', args.port))
        server_socket.listen(1)

        print("Server is ready", file=sys.stderr)

        while True:
            connection_socket, addr = server_socket.accept()
            threading.Thread(target=listen, args=(connection_socket, addr)).start()

def http_handle(request_string):
    """Given a http request return a response
    Both request and response are unicode strings with platform standard
    line endings.
    """
    filename = request_string.split()[1]
    filename = "index.html" if filename == '/' else filename[1:]

    print("filename {}".format(filename))

    with open(filename) as f:
        output_data = f.read()
    return output_data

if __name__ == '__main__':
    main()