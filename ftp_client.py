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
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp == "221 Closing session.\r\n":
                client_command_socket.close()
        else:
            pass
        break


    elif command == "ascii":
        send_recv_print_cmd("TYPE A\r\n")
    
    elif command == "binary":
        send_recv_print_cmd("TYPE I\r\n")

    elif command == "bye":
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp == "221 Closing session.\r\n":
                client_command_socket.close()
        else:
            pass
        break
    
    elif command == "cd":
        try:
            input_path = user_input[1]
        except IndexError:              # case user didn't type "path"
            input_path = input("Remote directory ")
        
        send_recv_print_cmd(f"CWD {input_path}\r\n")


    elif command == "close":        #close session and return to FTP
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp == "221 Closing session.\r\n":
                client_command_socket.close()
                pass
        else:
            print("Not connected.")
        

    elif command == "delete":
        pass

    elif command == "disconnect":    #close session and return to FTP
        if connect_status == True:
            resp = send_recv_print_cmd("QUIT\r\n")
            if resp == "221 Closing session.\r\n":
                client_command_socket.close()
                pass
        else:
            print("Not connected.")
        


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

        try:
            client_command_socket.connect((user_input[1], server_command_port))
        except gaierror:
            print(f"Unknow host {user_input[1]}.")
            continue

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
            client_data_socket.bind(('', 0))
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
                try:
                    input_path = user_input[1]
                    client_command_socket.send(f"NLST {input_path}\r\n".encode())
                except IndexError:
                    client_command_socket.send("NLST\r\n".encode())
                
                cmd_rep = client_command_socket.recv(2047).decode()
                print(cmd_rep, end='')
                data_income = connection_socket.recv(2047).decode()
                data_income_lenght = len(data_income)
                connection_socket.close()
                cmd_rep_2 = client_command_socket.recv(2047).decode()
                print(data_income, end="")
                print(cmd_rep_2, end=f'ftp> {data_income_lenght} bytes received in 0.00Seconds 10.00Kbytes/sec.\n')



        else:
            print('Not connected.')


    elif command == "get":

        if connect_status == True:
            client_data_socket = socket(AF_INET, SOCK_STREAM)        # create data socket
            client_data_socket.bind(('', 0))
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
                client_command_socket.send(f"RETR {user_input[1]}\r\n".encode())
                cmd_rep = client_command_socket.recv(2047).decode()
                print(cmd_rep, end='')
                if cmd_rep != "550 No such file.\r\n":
                    data_income = connection_socket.recv(2047).decode()
                    data_income_lenght = len(data_income)
                    connection_socket.close()
                    cmd_rep_2 = client_command_socket.recv(2047).decode()
                    print(cmd_rep_2, end=f'ftp> {data_income_lenght} bytes received in 0.00Seconds 10.00Kbytes/sec.\n')

                    try:
                        filename = user_input[2]
                    except IndexError:
                        filename = user_input[1]
                    f = open(filename, "w")
                    f.write(data_income)
                    f.close()
                else:
                    connection_socket.close()

        else:
            print('Not connected.')


    elif command == "pwd":
        send_recv_print_cmd("XPWD\r\n")



                



        


            
            
            








