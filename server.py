import socket
import json
import datetime


class Server:
    all_users = []
    admin_password = "becomeanadmin"
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
            if data == "admin" and user != None and user.admin == True:
                self.admin_panel(connection)
            elif data == self.admin_password:
                user.admin = True
                connection.send("You have authenticated, you are given administrator privileges".encode("utf8"))
            elif data == "create" and user == None:
                self.create_account(client_socket)
            elif data == "login" and user == None:
                user = self.login(client_socket)
            elif data == "send" and user != None:
                self.send_message(client_socket, user)
            elif data == "read" and user != None:
                self.read_message(connection, user)
            elif data == "clear" and user != None:
                self.clear_inbox(connection, user)
            elif data == "uptime":
                connection.send(bytes(json.dumps(self.commands(user)[0]), encoding="utf8"))
            elif data == "info":
                connection.send(bytes(json.dumps(self.commands(user)[1]), encoding="utf8"))
            elif data == "help":
                connection.send(bytes(json.dumps(self.commands(user)[2]), encoding="utf8"))
            elif data == "stop":
                connection.send("Stop the client".encode("utf8"))
                print("Server is turning off")
                with open("users.json", "w") as data:
                    json.dump(self.all_users, data, default=lambda u: u.user_to_dict()) 
                break
            elif data == "off" and user != None:
                print(f"[{client_socket.address[0]}:{client_socket.address[1]}] User \"{user.name}\" has been logged out")
                user = None
                connection.send("Logged out".encode("utf8"))
            else:
                connection.send(bytes(json.dumps(self.commands(user)[3]), encoding="utf8"))
                continue

    def commands(self, user):
        uptime = {"Uptime": str(datetime.datetime.now() - self.start_time)}
        info = {"Title": "My First Client/Server Application", "Version": "1.1.0", "Date created": "21.12.2022"}
        help = {"create": "create your account", "login": "Log in to your account", "uptime": "show the server's uptime", "info": "show the server's info", "help": "show all available commands", "stop": "stop the server"}
        unknown_command = {"[Error]": "Unknown command, please try again"}
        if user != None:
            del help["create"]
            del help["login"]
            help = {"send": "send a message to the user", "read": "read your messages", "clear": "remove all your messages", **help, "off": "log out of your account"}

        self.all_commands = [uptime, info, help, unknown_command]
        return self.all_commands

    def admin_panel(self, connection):
        connection.send("Admin panel".encode("utf8"))

        commands = {"reset": "reset user's password", "sendall": "send message to all users", "readfor": "read user's inbox", "delete": "delete user account"}
        connection.send(bytes(json.dumps(commands), encoding="utf8"))
        while True:
            command = connection.recv(1024)
            command = command.decode("utf8")
            if command == "reset":
                self.reset_password(connection)
            elif command == "sendall":
                self.send_to_all(connection)
            elif command == "readfor":
                self.read_for(connection)
            elif command == "delete":
                self.delete_user(connection)
            elif command == "off":
                connection.send(command.encode("utf8"))
                return
            else:
                connection.send("Unknown command, please try again".encode("utf8"))

    def reset_password(self, connection):
        connection.send("reset password".encode("utf8"))
        user_name = connection.recv(1024)
        user_name = user_name.decode("utf8")

        for user in self.all_users:
            if user.name == user_name:
                user.password = "newpassword"
                user.mail_box.append(("type your new password", "Admin"))
    
    def send_to_all(self, connection):
        connection.send("sendtoall".encode("utf8"))
        message_content = connection.recv(1024)
        message_content = message_content.decode("utf8")

        for user in self.all_users:
            if user.admin == False:
                user.mail_box.append((message_content, "Admin"))
    
    def read_for(self, connection):
        connection.send("readfor".encode("utf8"))
        username = connection.recv(1024)
        username = username.decode("utf8")

        for user in self.all_users:
            user_inbox = dict()
            if user.name == username:
                for message in user.mail_box:
                    user_inbox[message[0]] = message[1]
        user_inbox = json.dumps(user_inbox)
        connection.send(bytes(user_inbox, encoding="utf8"))

    def delete_user(self, connection):
        connection.send("delete".encode("utf8"))
        username = connection.recv(1024)
        username = username.decode("utf8")

        for user in self.all_users:
            if user.name == username:
                self.all_users.remove(user)
                del user
                connection.send("User has been deleted".encode("utf8"))
                return
        connection.send("User not found".encode("utf8"))

        
    def create_account(self, client_socket):
        connection = client_socket.connection
        connection.send("Create account".encode("utf8"))

        while True:
            data = connection.recv(1024)
            account_data = json.loads(data)
            for key, value in account_data.items():
                found = False
                for user in self.all_users:
                    if user.name == key:
                        found = True
                        break
                if not found and key != "admin" and value != "reset":
                    User(key, value, False, list())
                    connection.send("done".encode("utf8"))
                    print(f"[{client_socket.address[0]}:{client_socket.address[1]}] Account \"{key}\" created")
                    return
                else:
                    connection.send("wrong".encode("utf8"))
            

    def login(self, client_socket):
        connection = client_socket.connection
        connection.send("Log in".encode("utf8"))

        while True:
            data = connection.recv(1024)
            login_data = json.loads(data)
            for name, password in login_data.items():
                if password == "reset":
                    for user in self.all_users:
                        if user.admin == True:
                            user.mail_box.append(("[PASSWORD RESET REQUEST]", name))
                            return
                for user in self.all_users:
                    if user.name == name and user.password == password:
                        connection.send("done".encode("utf8"))
                        print(f"[{client_socket.address[0]}:{client_socket.address[1]}] Account \"{user.name}\" has been logged")
                        return user
            connection.send("wrong".encode("utf8"))
        
    def send_message(self, client_socket, user):
        connection = client_socket.connection
        connection.send("Send a message".encode("utf8"))
        data = connection.recv(1024)
        message_data = json.loads(data)
        for name, message in message_data.items():
            if name == user.name:
                connection.send("You can't send a message to yourself".encode("utf8"))
                return
            elif name == "admin":
                for admin in self.all_users:
                    if admin.admin == True:
                        admin.mail_box.append((message, user.name))
                connection.send("Sent".encode("utf8"))
                return
            else:
                for recipient in self.all_users:
                    if name == recipient.name:
                        if len(recipient.mail_box) >= 5 and recipient.admin == False:
                            connection.send("The recipient's inbox is full, you cannot send the message".encode("utf8"))
                            return
                        connection.send("Sent".encode("utf8"))
                        recipient.mail_box.append((message, user.name)) 
                        print(f"[{client_socket.address[0]}:{client_socket.address[1]}] User {user.name} sent message to {name}")
                        return
                connection.send("There is no such user".encode("utf8"))  
        return

    def read_message(self, connection, user):
        connection.send("Read a message".encode("utf8"))
        message = dict()
        reset_password = False
        if len(user.mail_box) == 0:
            message = {"[INFO]": "You don't have any messages"}
        else:
            for item in user.mail_box:
                if item[0] == "type your new password":
                    reset_password = True
                message[item[0]] = f"from [{item[1]}]"
        message = json.dumps(message)
        connection.send(bytes(message, encoding="utf8"))
        if reset_password == False:
            return
        elif reset_password:
            new_password = connection.recv(1024)
            new_password = new_password.decode("utf8")
            user.password = new_password
        return

    def clear_inbox(self, connection, user):
        user.mail_box.clear()
        connection.send("Your inbox is now empty".encode("utf8"))



class Client:
    def __init__(self, server):
        server_connection = server.create_connection()
        self.connection = server_connection[0]
        self.address = server_connection[1]


class User:
    def __init__(self, name, password, admin, mail_box):
        self.name = name
        self.password = password
        self.admin = admin
        self.mail_box = mail_box
        server.all_users.append(self)
    
    def user_to_dict(self):
        return {
        "name": self.name,
        "password": self.password,
        "admin": self.admin,
        "mail_box": self.mail_box
        }
    
    @classmethod
    def from_dict(cls, data):
        return cls(data["name"], data["password"], data["admin"], data["mail_box"])


server = Server(socket.gethostbyname(socket.gethostname()), 31415)
try:
    with open("users.json", "r") as data_file:
            data = json.load(data_file)
    server.all_users = [User.from_dict(d) for d in data]
except json.decoder.JSONDecodeError:
    server.all_users = []
client = Client(server)
server.server_menu(client)




