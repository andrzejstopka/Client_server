import datetime
import json
import socket
from database_config import database


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
            client_socket.send('Welcome to the server, type "help" to check all commands'.encode("utf8"))
            return client_socket, address

    def server_menu(self, client_socket):
        connection = client_socket.connection
        user = None
        while True:
            data = connection.recv(1024).decode("utf8")

            if data == "admin" and user is not None and user.admin is True:
                self.admin_panel(connection)

            elif data == self.admin_password and user is not None:
                user.admin = True
                database.become_admin(user.name)
                connection.send("You have authenticated, you are given administrator privileges".encode("utf8"))

           
            elif data == "create" and user is None:
                while True:
                    response = connection.recv(1024)
                    account_data = json.loads(response)
                    if self.create_account(account_data) == True:
                        connection.send("Account created succesfully".encode("utf8"))
                        user_name = list(account_data.keys())[0]
                        print(f'[{client_socket.address[0]}:{client_socket.address[1]}] Account "{user_name}" created')
                        break
                    else:
                        connection.send("Username is already taken. Try again.".encode("utf8")) 
            
            elif data == "login" and user is None:
                while True:
                    data = connection.recv(1024)
                    login_data = json.loads(data)
                    if self.login(login_data) != False:
                        user = self.login(login_data)
                        if user is None:
                            connection.send("Your password reset request has been sent. After the admin reset your password, log on with \"newpassword\" and go to your inbox to set the new password".encode("utf-8"))
                        else:
                            connection.send("Logged in successfully.".encode("utf8"))
                            print(f'[{client_socket.address[0]}:{client_socket.address[1]}] Account "{user.name}" has been logged')
                        break
                    else:
                        connection.send("Invalid username or password. Try again.".encode('utf-8'))
            
            
            elif data == "send" and user is not None:
                message_data = connection.recv(1024)
                message_data = json.loads(message_data)
                response = self.send_message(user, message_data)
                connection.send(response)
                if response == "Your message to admin has been sent!".encode("utf8"):
                    recipient_name = list(message_data.keys())[0]
                    print(f"[{client_socket.address[0]}:{client_socket.address[1]}] User {user.name} sent message to {recipient_name}")

            
            elif data == "read" and user is not None:
                response = self.read_message(user)
                response = json.dumps(response)
                connection.send(bytes(response, encoding="utf8"))
                if "type your new password" in response:
                    new_password = connection.recv(1024)
                    new_password = new_password.decode("utf8")
                    connection.send("Your password has been changed".encode("utf8"))
                    user.password = new_password
                    database.set_password(user.name, new_password)

            elif data == "clear" and user is not None:
                user.clear_inbox()
                connection.send("Your inbox is now empty".encode("utf8"))

                
            elif data == "uptime":
                connection.send(bytes(json.dumps(self.commands(user)[0]), encoding="utf8"))
            elif data == "info":
                connection.send(bytes(json.dumps(self.commands(user)[1]), encoding="utf8"))
            elif data == "help":
                connection.send(bytes(json.dumps(self.commands(user)[2]), encoding="utf8"))
            elif data == "stop":
                connection.send("Stop the client".encode("utf8"))
                connection.close()
                print("Server is turning off")
                break
            elif data == "off" and user is not None:
                connection.send("You have been logged out".encode("utf8"))
                print(f'[{client_socket.address[0]}:{client_socket.address[1]}] User "{user.name}" has been logged out')
                user = None
            else:
                connection.send(bytes(json.dumps(self.commands(user)[3]), encoding="utf8"))


    def commands(self, user):
        uptime = {"Uptime": str(datetime.datetime.now() - self.start_time)}
        info = {
            "Title": "My First Client/Server Application",
            "Version": "2.1.0",
            "Date created": "21.12.2022",
        }
        help = {
            "create": "create your account",
            "login": "Log in to your account",
            "uptime": "show the server's uptime",
            "info": "show the server's info",
            "help": "show all available commands",
            "stop": "stop the server",
        }
        unknown_command = {"[Error]": "Unknown command, please try again"}
        if user is not None:
            del help["create"]
            del help["login"]
            help = {
                "send": "send a message to the user",
                "read": "read your messages",
                "clear": "remove all your messages",
                **help,
                "off": "log out of your account",
            }

        self.all_commands = [uptime, info, help, unknown_command]
        return self.all_commands

    def admin_panel(self, connection):
        commands = {
            "reset": "reset user's password",
            "sendall": "send message to all users",
            "readfor": "read user's inbox",
            "delete": "delete user account",
        }
        connection.send(bytes(json.dumps(commands), encoding="utf8"))
        while True:
            command = connection.recv(1024)
            command = command.decode("utf8")
            if command == "reset":
                user_name = connection.recv(1024)
                user_name = user_name.decode("utf8")
                self.reset_password(user_name)
                connection.send(f"Password user {user_name} has been reset".encode("utf8"))

            elif command == "sendall":
                message_content = connection.recv(1024)
                message_content = message_content.decode("utf8")
                self.send_to_all(message_content)
                connection.send(("Your message has been sent to all".encode("utf8")))

            elif command == "readfor":
                username = connection.recv(1024)
                username = username.decode("utf8")
                connection.send(bytes(self.read_for(username), encoding="utf8"))


            elif command == "delete":
                username = connection.recv(1024)
                username = username.decode("utf8")
                connection.send(self.delete_user(username))

            elif command == "off":
                connection.send("You disable the admin panel".encode("utf-8"))
                return
            else:
                connection.send("Unknown command, please try again".encode("utf8"))

    def reset_password(self, username):

        for user in self.all_users:
            if user.name == username:
                user.password = "newpassword"
                user.mail_box["type your new password"] = "Admin"
                database.reset_password(username)


    def send_to_all(self, message_content):
        for user in self.all_users:
            if user.admin is False:
                user.mail_box[message_content] = "Admin"
                database.send_to_all(message_content)

    def read_for(self, username):
        
        user_inbox = dict()
        for user in self.all_users:
            if user.name == username:
                if user.mail_box == {}:
                    user_inbox["[INFO]"] = "You don't have any messages"
                else:
                    user_inbox = user.mail_box
        if user_inbox == {}:
            user_inbox["[ERROR]"] = "User not found"
        user_inbox = json.dumps(user_inbox)
        return user_inbox

    def delete_user(self, username):
        for user in self.all_users:
            if user.name == username:
                self.all_users.remove(user)
                del user
                database.delete_user(username)
                return f"User {username} has been deleted".encode("utf8")
        return f"User {username} not found".encode("utf8")

    def create_account(self, account_data):

        for key, value in account_data.items():
            found = False
            for user in self.all_users:
                if user.name == key:
                    found = True
                    return False
            if not found and key != "admin" and value != "reset":
                User(key, value, False, dict())
                database.add_user(key, value, False, dict())
                return True

    def login(self, login_data):
        for name, password in login_data.items():
            if password == "reset":
                for user in self.all_users:
                    if user.admin is True:
                        user.mail_box["[PASSWORD RESET REQUEST]"] = name
                        return
            for user in self.all_users:
                if user.name == name and user.password == password:
                    return user
        return False

    def send_message(self, user, message_data):
        for name, message in message_data.items():
            if name == user.name:
                return "You can't send a message to yourself".encode("utf8")
            elif name == "admin":
                for admin in self.all_users:
                    if admin.admin is True:
                        admin.mail_box[message] = user.name
                return "Your message to admin has been sent!".encode("utf8")
            else:
                for recipient in self.all_users:
                    if name == recipient.name:
                        if len(recipient.mail_box) >= 5 and recipient.admin is False:
                            return "The recipient's inbox is full, you cannot send the message".encode("utf8")
                        recipient.mail_box[message] = user.name
                        database.send_message({message: user.name}, recipient.name)
                        return "Your message has been sent!".encode("utf-8")
                return "There is no such user".encode("utf8")

    def read_message(self, user):
        message = dict()
        reset_password = False
        if len(user.mail_box) == 0:
            return {"[INFO]": "You don't have any messages"}
        else:
            for item in user.mail_box.items():
                if item[0] == "type your new password":
                    set_new_password = {item[0]: item[1]}
                    reset_password = True
                message[item[0]] = f"from [{item[1]}]"
        if reset_password is False:
            return message
        elif reset_password:
            del user.mail_box["type your new password"]
            return set_new_password
            



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
            "mail_box": self.mail_box,
        }

    def clear_inbox(self):
        self.mail_box = []

server = Server(socket.gethostbyname(socket.gethostname()), 31415)
if __name__ == "__main__":
    data = database.load_data()
    server.all_users = [User(row[0], row[1], row[2], row[3]) for row in data]
    client = Client(server)
    server.server_menu(client)
