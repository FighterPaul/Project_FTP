from socket import *
from getpass import *
current_ip_address = "127.0.0.1"
buff_size = 2047

connect_status = False
current_ftp_host = ""

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

    if command == "open":     # open [ip] [port]
            if connect_status == True:
                print(f"Already connected to {current_ftp_host}, use disconnect first.")
                continue
            else:
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
                except OSError:
                    print("> ftp: connect :Connection refused")
                    continue

                connection_response_message = client_command_socket.recv(2047).decode()
                if connection_response_message[0:3] == "220":
                    print(f"Connected to {user_input[1]}.")
                print(connection_response_message, end='')
                connect_status = True
                current_ftp_host = user_input[1]

                # if connectiob is established -> OPTS UTF8 ON 
                if connection_response_message[0:3] == "220":
                    send_recv_print_cmd("OPTS UTF8 ON\r\n")

                # if connectiob is established -> LOGIN 
                if connection_response_message[0:3] == "220":
                    username = input(f"User ({user_input[1]}:(none)): ")
                    resp = send_recv_print_cmd(f"USER {username}\r\n")

                    if resp[0:3] == "331":     # 331 password required
                        password = getpass()
                        resp = send_recv_print_cmd(f"PASS {password}\r\n")

                        if resp[0:3] == "230":     # LOGIN SUCCESS
                            pass
                        elif resp[0:3] == "530":    # 530 Authentication rejected 
                            print("Login failed.") 

                    elif resp[0:3] == "501":    # 501 User name not specified
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

           
            client_command_socket.send("NLST \r\n".encode())
            connection_socket, ser_addr = client_data_socket.accept()      # wait 3 way hand shake from server

            cmd_rep = client_command_socket.recv(2047).decode()     # get recv response from ls command
            print(cmd_rep, end='')                                  # print ls command response



            # data_income = connection_socket.recv(2047).decode()     # recv data

            # data_income_lenght = len(data_income)                   # count data byte

            # connection_socket.close()                               # close actual_data_socket

            # cmd_rep_2 = client_command_socket.recv(2047).decode()   # recv respone "226 Transfer complete"


            # try:                                    # case user type [local file]
            #     local_file = user_input[2]
            #     f = open(local_file, "w", newline='')
            #     f.write(data_income)
            #     f.close()
                
            # except IndexError:                       # case user didn't type [local file]
            #     print(data_income, end="")                              #print data
                
            # print(cmd_rep_2, end=f'ftp> {data_income_lenght} bytes received in 0.00Seconds 10.00Kbytes/sec.\n') #print statistic


                



        


            
            
            








