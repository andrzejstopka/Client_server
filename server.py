import socket
import json
import datetime


class Server:
    all_users = []
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.start_time = datetime.datetime.now()

    def create_connection(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen()
            print("Server listening on...")
            client_socket, address = server_socket.accept()
            print(f"Client connected from {address[0]}:{address[1]}")
            client_socket.send("Welcome to the server, type \"help\" to check all commands".encode("utf8"))
            return client_socket

    def server_menu(self, client_socket):
        while True:
            data = client_socket.recv(1024).decode('utf8')
            if data == "create":
                self.create_account(client_socket)
                continue
            elif data == "uptime":
                client_socket.send(bytes(json.dumps(self.commands()[0]), encoding="utf8"))
                continue
            elif data == "info":
                msg = info()
            elif data == "help":
                msg = help()
            elif data == "stop":
                client_socket.send("Stop the client".encode("utf8"))
                print("Server is turning off")
                break
            else:
                print(f"Unknown command: {data}")
                continue
            if data != "stop":
                msg = json.dumps(msg)
                client_socket.send(bytes(msg, encoding="utf8"))

    def commands(self):
        uptime = {"Uptime": str(datetime.datetime.now() - self.start_time)}
        info = {"Title": "My First Client/Server Application", "Version": "1.0.0", "Date created": "21.12.2022"}
        help = {"create": "create your account", "login": "Log in to your account", "uptime": "show the server's uptime", "info": "show the server's info", "help": "show all available commands", "stop": "stop the server"}
        # if user.logged == True:
        #     del help["create"]
        #     del help["login"]
        #     {"read": "read your messages"}.update(help)
        #     {"send": "send a message"}.update(help)
        self.all_commands = [uptime, info, help]
        return self.all_commands

    ZROBIĆ W KLASIE USERA POŁĄCZENIE Z SOCKETEM ABY USPRAWNIĆ LOGOWANIE 
    DOKOŃCZYĆ PODPINANIE FUNKCJI MENU GŁÓWNEGO

    def create_account(self, client_socket):
        client_socket.send("Create account".encode("utf8"))
        data = client_socket.recv(1024)
        account_data = json.loads(data)
        for key, value in account_data.items():
            User(key, value, False)
                
class User:
    def __init__(self, name, password, admin):
        self.name = name
        self.password = password
        self.admin = admin
        self.mail_box = []
        self.logged = False
        self.add_to_all_users()
    
    def add_to_all_users(self):
        Server.all_users.append({self.name: [self.password, self.admin, self.mail_box]})

def uptime(start):
    start_time = start
    now_time = datetime.datetime.now()
    uptime = {"Uptime": str(now_time - start_time)}
    return uptime

def info():
    info = {"Title": "My First Client/Server Application", 
    "Version": "1.0.0",
    "Date created": "21.12.2022"
    }
    return info

def help():
    help = {"uptime": "show the server's uptime",
    "info": "show the server's info",
    "help": "show all available commands",
    "stop": "stop the server"}
    return help

def stop():
    pass


# HOST = socket.gethostbyname(socket.gethostname())
# PORT = 31415


server = Server(socket.gethostbyname(socket.gethostname()), 31415)
# server.create_connection()
server.server_menu(server.create_connection())
# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
#     server_socket.bind((HOST, PORT))
#     server_socket.listen()
#     print("Server listening on...")
#     client_socket, address = server_socket.accept()
#     start_time = datetime.datetime.now()
#     print(f"Client connected from {address[0]}:{address[1]}")
#     client_socket.send("Welcome to the server, type \"help\" to check all commands".encode("utf8"))
    # while True:
    #     data = client_socket.recv(1024).decode('utf8')
    #     if data == "create":
    #         client_socket.send("Create account".encode("utf8"))
    #         data = client_socket.recv(1024)
    #         account_data = json.loads(data)
    #         for key, value in account_data.items():
    #             User(key, value, False)
    #         continue
    #     elif data == "uptime":
    #         msg = uptime(start_time)
    #     elif data == "info":
    #         msg = info()
    #     elif data == "help":
    #         msg = help()
    #     elif data == "stop":
    #         client_socket.send("Stop the client".encode("utf8"))
    #         print("Server is turning off")
    #         server_socket.close()
    #         break
    #     else:
    #         print(f"Unknown command: {data}")
    #         continue
    #     if data != "stop":
    #         msg = json.dumps(msg)
    #         client_socket.send(bytes(msg, encoding="utf8"))




