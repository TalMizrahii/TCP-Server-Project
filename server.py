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
server.bind(('', 12345))
server.listen(5)


def search_file(patch_search, status):
    # if patch_file == 'redirect':
    #     return 'HTTP/1.1 301 Moved Permanently\nConnection: close\nLocation: /result.html\n\n'
    # Try to open and read in binary the file from the 'files' folder.
    try:
        file = open(patch_search, 'rb')
    # If the file does not exist, send a message and close the socket.
    except IOError:
        # return 'HTTP/1.1 404 Not Found\nConnection: close\n\n'
        pass
        return

        # Read the data from the file in binary.
    content = file.read()
    # Save the length of the file's content.
    content_length = str(len(content))
    # Create the response message.
    # format_resend1 = 'HTTP/1.1 200 OK\nConnection: ' + status + '\nContent-Length: ' + content_length + '\n\n'

    format_resend1 = 'HTTP/1.1 200 OK\nConnection: ' + status + '\nContent-Length: '
    format_resend2 = content_length + '\n\n'

    result = format_resend1.encode() + format_resend2.encode() + content
    return result, int(content_length)

    # Return the response.
    # return format_resend1.encode() + content


def extract_path_and_conn(client_data):
    # Spiting the request from the client.
    data_list = client_data.split(' ')
    # DELETE - Check only.
    print(data_list)
    #
    path = data_list[1]
    index_of_loop = 2
    # Scan the split data until you see the end of the request.
    while data_list[index_of_loop] != 'HTTP/1.1\r\nHost:':
        # Add the spaces removed by the "split".
        path += ' '
        # Keep scanning.
        path += data_list[index_of_loop]
        index_of_loop += 1
    # Step over the http format to the connection segment.
    index_of_loop += 2
    # Save the connection status.
    connection = data_list[index_of_loop]
    connection = connection.split('\r')[0]
    # Save the path without the starting '/'.
    path = path[1:]
    return path, connection


def main():
    while True:
        client_socket, client_address = server.accept()
        client_socket.settimeout(10.0)
        print('Connection from: ', client_address)
        try:
            data = client_socket.recv(100).decode()
        except:
            # CLOSE
            client_socket.close()
            continue

        print('Received: ', data)
        patch_file, connection_status = extract_path_and_conn(data)

        response_data, response_length = search_file(patch_file, connection_status)
        response_data_array = bytearray(response_data)
        size_to_send = 100
        while response_length > size_to_send:
            client_socket.send(response_data_array[size_to_send - 100: size_to_send])
            size_to_send += 100

        print("\n\n")


if __name__ == '__main__':
    main()
