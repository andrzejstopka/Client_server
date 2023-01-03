import json
import socket

import pwinput


def admin_panel():
    print("Admin Panel")
    commands = client_socket.recv(1024)
    for key, value in json.loads(commands).items():
        print(f"{key} - {value}")
    while True:
        admin_command = input("Type the command: ")
        client_socket.send(admin_command.encode("utf8"))
        
        if admin_command == "reset":
            reset_password()
        elif admin_command == "sendall":
            send_to_all()
        elif admin_command == "readfor":
            read_for()
        elif admin_command == "delete":
            delete_user()
        elif admin_command == "off":
            response = client_socket.recv(1024)
            print(response.decode("utf-8"))
            return
        else:
            print("Unknown command, please try again")


def reset_password():
    user_name = input("Enter user name to reset his password: ").strip()
    client_socket.send(user_name.encode("utf8"))
    response = client_socket.recv(1024)
    print(response.decode("utf8"))


def send_to_all():
    message_content = input("Your message: ")
    client_socket.send(message_content.encode("utf8"))
    response = client_socket.recv(1024)
    print(response.decode("utf8"))


def read_for():
    read_for_user = input("Enter the username to read his messages: ").strip()
    client_socket.send(read_for_user.encode("utf8"))
    user_inbox = client_socket.recv(1024)
    user_inbox = json.loads(user_inbox)

    for key, value in user_inbox.items():
        print(f"{key} from [{value}]")


def delete_user():
    username = input("Enter the username to delete: ").strip()
    client_socket.send(username.encode("utf8"))
    server_answer = client_socket.recv(1024)
    print(server_answer.decode("utf8"))


def create_account():
    print("[CREATE YOUR ACCOUNT]")
    while True:
        name = input("Name: ").strip()
        password = pwinput.pwinput(prompt="Password: ", mask="*")
        account_data = json.dumps({name: password})
        client_socket.send(bytes(account_data, encoding="utf8"))

        response = client_socket.recv(1024)
        response = response.decode("utf8")
        print(response)
        if response == "Account created succesfully":
            break
        


def log_in():
    print("[LOGIN YOUR ACCOUNT]")
    while True:
        name = input("Name: ").strip()
        password = pwinput.pwinput(prompt='Password (if you want to reset your password type here "reset"): ',mask="*",)
        login_data = json.dumps({name: password})
        client_socket.send(bytes(login_data, encoding="utf8"))
    
        response = client_socket.recv(1024)
        response = response.decode("utf8")
        print(response)
        if response != "Invalid username or password. Try again.":
            break
            


def send_message():
    print("[SEND A MESSAGE]")
    recipient = input('Enter an username (if you want to send a message to the administrator type "admin"): ').strip()
    message = input("Enter a message: ")
    message_data = json.dumps({recipient: message})
    client_socket.send(bytes(message_data, encoding="utf-8"))
    response = client_socket.recv(1024)
    response = response.decode("utf8")
    print(response)


def read_message():
    print("[YOUR MAIL BOX]")
    message = client_socket.recv(1024)
    message = json.loads(message)
    if "type your new password" in message:
        print("You must enter your new password")
        new_password = pwinput.pwinput(prompt="Enter your new password: ", mask="*")
        client_socket.send(new_password.encode("utf-8"))
        response = client_socket.recv(1024)
        print(response.decode("utf-8"))
    else:
        for key, value in message.items():
            print(key, value)
    
HOST = socket.gethostbyname(socket.gethostname())
PORT = 31415

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
hello_message = client_socket.recv(1024).decode("utf-8")
print(hello_message)
while True:
    data = input("Enter the command: ")
    print()
    client_socket.send(data.encode("utf-8"))
    if data == "admin":
        admin_panel()
    elif data == "becomeanadmin":
        print(client_socket.recv(1024).decode("utf-8"))
    elif data == "create":
        create_account()
    elif data == "login":
        log_in()
    elif data == "send":
        send_message()
    elif data == "read":
        read_message()
    elif data == "clear":
        response = client_socket.recv(1024).decode("utf-8")
        print(response)
    elif data == "off":
        response = client_socket.recv(1024).decode("utf-8")
        if "Error" in response:
            print("[Error] Unknown command, please try again")
        else:
            print(response)
    elif data == "stop":
        print("Goodbye!")
        client_socket.close()
        break
    else:
        msg = client_socket.recv(1024)
        msg = msg.decode("utf-8")
        for key, value in json.loads(msg).items():
            print(f"{key}: {value}")
    print()
