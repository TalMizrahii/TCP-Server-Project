
import socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('', 12345))
server.listen(5)

while True:
    client_socket, client_address = server.accept()
    print('Connection from: ', client_address)
    data = client_socket.recv(100).decode()
    print('Received: ', data)
    dataList = data.split(' ')
    i = 2
    patchFile = dataList[1]
    while dataList[i] != 'HTTP/1.1\r\nHost:':
        patchFile += dataList[i]
    print(patchFile)
    client_socket.close()
    print('Client disconnected\n')