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


def search_file(patch_search, status):
    if patch_file == '/redirect':
        return 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\n\n'
    file = open(patch_search, 'rb')
    content = file.read()
    content_length = str(len(content))

    format_resend1 = 'HTTP/1.1 200 OK\nConnection: ' + status + '\nContent-Length: '
    format_resend2 = '\n\n'

    result = format_resend1.encode() + content_length.encode() + format_resend2.encode() + content
    return result


def extract_patch_and_conn(client_data):
    data_list = client_data.split(' ')
    print(data_list)
    i = 2
    patch = data_list[1]
    while data_list[i] != 'HTTP/1.1\r\nHost:':
        patch += data_list[i]
        patch += ' '
        i += 1

    connection = data_list[4]
    connection = connection.split('\r')[0]
    patch = patch[1:]
    return patch, connection


if __name__ == '__main__':

    while True:
        client_socket, client_address = server.accept()
        print('Connection from: ', client_address)
        data = client_socket.recv(100).decode()
        print('Received: ', data)
        patch_file, connection_status = extract_patch_and_conn(data)
        client_socket.send(search_file(patch_file, connection_status))

        print('Client disconnected\n')
