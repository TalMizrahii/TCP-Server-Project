import socket
import os
import sys

'''
# Opening the server's socket.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Getting the port from the system.
server_port = str(sys.argv[1])
# If the port is not valid, exit the program.
if not server_port.isnumeric() or (int(server_port) not in range(0, 65536)):
    exit(0)
# Binding the server port (received from the sys).
s.bind(('', int(server_port)))
'''
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12344))
server.listen(5)


def search_file(path_search, status):
    if path_search == '/redirect':
        return 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\n\n'
    file = open(path_search, 'rb')
    content = file.read()
    content_length = str(len(content))

    format_resend1 = 'HTTP/1.1 200 OK\nConnection: ' + status + '\nContent-Length: '
    format_resend2 = '\n\n'

    result = format_resend1.encode() + content_length.encode() + format_resend2.encode() + content
    return result


def extract_path_and_conn(client_data):
    data_list = client_data.split(' ')
    i = 2
    path = data_list[1]
    while data_list[i] != 'HTTP/1.1\r\nHost:':
        path += data_list[i]
        path += ' '
        i += 1

    connection = data_list[4]
    connection = connection.split('\r')[0]
    path = path[1:]
    # If the client sent the char '/' he means the file 'index.html'.
    if path == '/':
        path = 'index.html'
    return path, connection


def close_client_socket(info):
    if info == '' or '/close' or 'HTTP/1.1 404 Not Found\nConnection: close\n\n':
        print('Client disconnected\n')
        client_socket.close()


if __name__ == '__main__':
    while True:
        # Creating the client's specific socket.
        client_socket, client_address = server.accept()
        # Setting timeout to the socket.
        client_socket.settimeout(10)
        # Printing the client's address by the requested format.
        print('Connection from: ', client_address)
        # Decoding the data he sent.
        data = client_socket.recv(100).decode()
        print('Received: ', data)
        # Extract the data and connection status from the client's request.
        path_file, connection_status = extract_path_and_conn(data)
        # If the client sent a message to close the program, execute.
        if close_client_socket(path_file):
            continue
        # If the request is about to search for a file, try to find it in the limits of the timeout.
        try:
            # Try to find the file.
            client_socket.send(search_file(path_file, connection_status))
        except client_socket.timeout:
            # If the timeout accord, close the socket.
            close_client_socket(path_file)



