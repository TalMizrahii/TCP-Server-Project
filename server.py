"""
Title: TCP server accepting browser clients.
Authors: Yuval Arbel, Tal Mizrahi.
Date: 04/12/2022.
Version: V1.0
"""

import socket
import sys

# Opening the server's socket.
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Getting the port from the system.
server_port = str(sys.argv[1])
# If the port is not valid, exit the program.
if not server_port.isnumeric() or (int(server_port) not in range(0, 65536)):
    exit(0)
# Binding the server port (received from the sys).
server.bind(('', int(server_port)))
server.listen(5)


# Searching for a file with path given by the client.
def search_file(path_search, status):
    # If the client sent 'redirect', we return to him the follow message.
    if path_search == 'files/redirect':
        return 'HTTP/1.1 301 Moved Permanently\r\nConnection: close\r\nLocation: /result.html\r\n\r\n'.encode(), 'close'
    # Try to open a file by the path given by the client.
    try:
        file = open(path_search, 'rb')
    # If the file does not exist, send a message and close the socket.
    except IOError:
        # Close func
        return 'HTTP/1.1 404 Not Found\nConnection: close\n\n'.encode(), 'close'
    # Read the data from the file in binary.
    content = file.read()
    # Save the length of the file's content.
    content_length = str(len(content))
    # Building a reply message to the user.
    format_resend1 = 'HTTP/1.1 200 OK\nConnection: ' + status + '\nContent-Length: '
    format_resend2 = content_length + '\n\n'
    # Encode the message into result.
    result = format_resend1.encode() + format_resend2.encode() + content
    # Return the result and the connection status.
    return result, status


# Extracting the client request for a path or a file from the whole request.
def extract_path_and_conn(data_list):
    # The file or path begins in index 1.
    path = data_list[1]
    # A counter for the while loop.
    index_of_loop = 2
    # Scan the data list until you see the end of the request.
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
    # Extract ht connection status.
    connection = connection.split('\r')[0]
    # Don't remove the first '/' if it's the whole message.
    if path == '/':
        return path, connection
    # Save the path without the starting '/'. and replace redundant '%20' with spaces.
    path = path[1:].replace("%20", " ")
    # If the client sends the message '/', he wants the file 'index.html'.
    if path == '/':
        path = 'files/index.html'
    # If the client wants a file by name and not by path, allow him.
    if path[0:5] != "files":
        path = 'files/' + path
    # Return the path and the connection status.
    return path, connection


# Send Data to the client while handling any timeout exceptions.
def send_to_client(sock):
    while True:
        # Trying to receive the client request.
        try:
            # Accept data from the socket.
            data = sock.recv(4096)
            # Checking if the user sent an empty data.
            if len(data) == 0:
                return
            # Keep receiving data as long we didn't receive "\r\n\r\n".
            while "\r\n\r\n" not in data.decode():
                data += sock.recv(4096)

        # If we did not get the client request in 1s timeout.
        except socket.timeout:
            return
        # Decode data to string representation.
        data = data.decode()
        # Split data.
        split_data = data.split(' ')
        # Checking if the data is a request or not.
        if split_data[0] != 'GET':
            continue
        # Printing the request from the client as asked.
        print(data)
        # Extracting the path/file name from the data.
        patch_file, connection_status = extract_path_and_conn(split_data)
        # Searching for the file in the system.
        response_data, status = search_file(patch_file, connection_status)
        # Checking with the flag if we need to close the client socket
        if status == 'close':
            sock.send(response_data)
            return
        # Returning the response.
        sock.send(response_data)


# The main control flow function of the program.
def main():
    while True:
        client_socket, client_address = server.accept()
        client_socket.settimeout(1.0)
        send_to_client(client_socket)
        client_socket.close()


# The main function.
if __name__ == '__main__':
    main()
