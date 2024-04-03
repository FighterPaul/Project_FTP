from socket import *
from getpass import *
current_ip_address = "192.168.1.54"
buff_size = 2047
connect_status = False
data_socket_status = False      




def send_recv_print_cmd(cmd: str):
    client_command_socket.send(cmd.encode())
    response = client_command_socket.recv(buff_size).decode()
    print(response, end='')
    return response





while True:

    user_input = input("ftp> ").strip()
    user_input = user_input.split(" ")

    command = user_input[0]

    if command == "quit":
        break
    
    elif command == "open":     # open [ip] [port]
        #create tcp socket
        client_command_socket = socket(AF_INET, SOCK_STREAM)
        #connect to ftp server port 21
        try:
            server_command_port = int(user_input[2])
        except IndexError:
            server_command_port = 21
        else:
            server_command_port = 21
        client_command_socket.connect((user_input[1], server_command_port))
        connection_response_message = client_command_socket.recv(2047).decode()
        print(connection_response_message, end='')

        # if connectiob is established -> OPTS UTF8 ON 
        if connection_response_message.split(" ")[0] == "220":
            send_recv_print_cmd("OPTS UTF8 ON\r\n")

        # if connectiob is established -> LOGIN 
        if connection_response_message.split(" ")[0] == "220":
            username = input(f"User ({user_input[1]}:(none)): ")
            resp = send_recv_print_cmd(f"USER {username}\r\n")

        if resp.split(" ")[0] == "331":     # 331 password required
            password = getpass()
            resp = send_recv_print_cmd(f"PASS {password}\r\n")

            if resp.split(' ')[0] == "230":     # LOGIN SUCCESS
                connect_status = True
            elif resp.split(' ')[0] == "530":    # 530 Authentication rejected
                print("Login failed.")




    elif command == "ls":

        # if connection is established then give a new port number to ftp server for make data connection
        if connect_status == True:
            client_data_socket = socket(AF_INET, SOCK_STREAM)        # create data socket
            client_data_socket.bind(('', 20000))
            client_data_socket.listen(1)


            #make PORT command
            data_socket_info = client_data_socket.getsockname()     # get ([ip], port)
            fragment_current_ip = current_ip_address.split('.')
            client_data_socket_port = int(data_socket_info[1])
            port_command = f"PORT {fragment_current_ip[0]},{fragment_current_ip[1]},{fragment_current_ip[2]},{fragment_current_ip[3]},{client_data_socket_port // 256},{client_data_socket_port % 256}\r\n"
            
            resp = send_recv_print_cmd(port_command)                # send data socket port to server
            connection_socket, ser_addr  = client_data_socket.accept()      # wait 3 way hand shake from server




            if resp.split(' ')[0] == "200":     # if after send port and 200 PORT OK
                data_socket_status = True


            if data_socket_status == True:      # if after create data socket
                client_command_socket.send("NLST\r\n".encode())
                cmd_rep = client_command_socket.recv(2047).decode()
                print(cmd_rep, end='')
                data_income = connection_socket.recv(2047).decode()
                print(data_income)

                

                


        else:
            print('Not connected.')


        


            
            
            


    
    elif command == "disconnect":
        client_command_socket.close()
        client_data_socket.close()
        connect_status = False
        data_socket_status = False
        





