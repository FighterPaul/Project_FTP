from socket import *

serverName = "127.0.0.1"

serverPort = 12001

client_socket = socket(AF_INET, SOCK_STREAM)

client_socket.connect((serverName, serverPort))

message = input("Enter message (lower case) : ")

client_socket.send(message.encode())

modified_message = client_socket.recv(2047)

print(f"message uppercase : {modified_message.decode()}")

client_socket.close()