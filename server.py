import socket
import os
import sys

# Opening the server's socket.
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Getting the port from the system.
server_port = str(sys.argv[1])
# If the port is not valid, exit the program.
if not server_port.isnumeric() or (int(server_port) not in range(0, 65536)):
    exit(0)
# Binding the server port (received from the sys).
s.bind(('', int(server_port)))

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12245))
server.listen(5)


def extract_patch_and_conn(client_data):
    data_list = client_data.split(' ')
    i = 2
    patch = data_list[1]
    while data_list[i] != 'HTTP/1.1\r\nHost:':
        patch += data_list[i]
    connection = data_list[4]
    connection = connection.split('\r')[0]
    return patch, connection


if __name__ == '__main__':

    while True:
        client_socket, client_address = server.accept()
        print('Connection from: ', client_address)
        data = client_socket.recv(100).decode()
        print('Received: ', data)
        patch_file, connection_status = extract_patch_and_conn(data)
        print(patch_file)
        print(connection_status)
        if patch_file == ' /redirect':
            client_socket.send('HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\n')
        client_socket.close()
        print('Client disconnected\n')
