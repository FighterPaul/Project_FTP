from socket import *

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)

message = input("Enter message (lower case): ")

message = message.encode()
clientSocket.sendto(message, (serverName, serverPort))

modifiedMessage, server_addr = clientSocket.recvfrom(2048)

print(modifiedMessage)
print(modifiedMessage.decode())


clientSocket.close()


