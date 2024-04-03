from socket import *

serverPort = 12001

serverSocket = socket(AF_INET, SOCK_STREAM)

serverSocket.bind(("", serverPort))

serverSocket.listen(1)

print("server ready to operate")

while(True):
    connection_socket, addr = serverSocket.accept()

    sentence = connection_socket.recv(2047)

    modified_sentence = sentence.decode().upper()

    connection_socket.send(modified_sentence.encode())

    connection_socket.close()