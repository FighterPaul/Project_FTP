from socket import *


serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)

serverSocket.bind(('', serverPort))

print("Server ready to running")

while (True):
    message_incoming, client_addr = serverSocket.recvfrom(2048)

    modified_message = message_incoming.decode().upper()
    
    serverSocket.sendto(modified_message.encode(), client_addr)

    print(f"send to {modified_message} with message: {client_addr}")


