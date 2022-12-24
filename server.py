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
            return client_socket, address

    def server_menu(self, client_socket):
        connection = client_socket.connection
        user = None
        while True:
            data = connection.recv(1024).decode('utf8')
            if data == "create":
                self.create_account(client_socket)
            elif data == "login":
                user = self.login(client_socket)
            elif data == "send":
                self.send_message(client_socket)
            elif data == "read":
                self.read_message(client_socket, user)
            elif data == "uptime":
                connection.send(bytes(json.dumps(self.commands(client_socket)[0]), encoding="utf8"))
            elif data == "info":
                connection.send(bytes(json.dumps(self.commands(client_socket)[1]), encoding="utf8"))
            elif data == "help":
                connection.send(bytes(json.dumps(self.commands(client_socket)[2]), encoding="utf8"))
            elif data == "stop":
                connection.send("Stop the client".encode("utf8"))
                print("Server is turning off")
                break
            else:
                connection.send(bytes(json.dumps(self.commands(client_socket)[3]), encoding="utf8"))
                continue

    def commands(self, client):
        uptime = {"Uptime": str(datetime.datetime.now() - self.start_time)}
        info = {"Title": "My First Client/Server Application", "Version": "1.0.0", "Date created": "21.12.2022"}
        help = {"create": "create your account", "login": "Log in to your account", "uptime": "show the server's uptime", "info": "show the server's info", "help": "show all available commands", "stop": "stop the server"}
        unknown_command = {"[Error]": "Unknown command, please try again"}
        if client.logged:
            del help["create"]
            del help["login"]
            help = {"send": "send a message to the user", "read": "read your messages", **help}

        self.all_commands = [uptime, info, help, unknown_command]
        return self.all_commands


    def create_account(self, client_socket):
        connection = client_socket.connection
        connection.send("Create account".encode("utf8"))
        data = connection.recv(1024)
        account_data = json.loads(data)
        for key, value in account_data.items():
            User(key, value, False, client_socket)
            print(f"[{client_socket.address[0]}:{client_socket.address[1]}] Account \"{key}\" created")

    def login(self, client_socket):
        connection = client_socket.connection
        connection.send("Log in".encode("utf8"))
        data = connection.recv(1024)
        login_data = json.loads(data)
        for name, password in login_data.items():
            for user in self.all_users:
                for username, user_data in user.items():
                    if username == name and user_data[0] == password:
                        print(f"[{client_socket.address[0]}:{client_socket.address[1]}] Account \"{username}\" has been logged")
                        return user

    def send_message(self, client_socket):
        connection = client_socket.connection
        connection.send("Send a message".encode("utf8"))
        data = connection.recv(1024)
        message_data = json.loads(data)
        for name, message in message_data.items():
            for user in self.all_users:
                if name == user.name:
                    user.mail_box.append(message)
                    return
        connection.send("There is no such user".encode("utf8"))  
    
    

class Client:
    def __init__(self, server):
        server_connection = server.create_connection()
        self.connection = server_connection[0]
        self.address = server_connection[1]
        self.logged = False


class User:
    def __init__(self, name, password, admin, client):
        self.name = name
        self.password = password
        self.admin = admin
        self.mail_box = []
        client.logged = True
        server.all_users.append(self)
    


server = Server(socket.gethostbyname(socket.gethostname()), 31415)
client = Client(server)
# user1 = User("andrzej", "stopka", False, client)
server.server_menu(client)




