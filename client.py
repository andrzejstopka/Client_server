import socket
import json
import pwinput

def admin_panel():
    print("Admin Panel")
    commands = client_socket.recv(1024)
    for key, value in json.loads(commands).items():
        print(f"{key} - {value}")
    while True:
        admin_command = input("Type the command: ")
        client_socket.send(admin_command.encode('utf8'))
        server_answer = client_socket.recv(1024)
        server_answer = server_answer.decode('utf8')

        if server_answer == "reset password":
            reset_password()
        elif server_answer == "sendtoall":
            send_to_all()
        elif server_answer == "readfor":
            read_for()
        elif server_answer == "delete":
            delete_user()
        elif server_answer == "off":
            return
        else:
            print(server_answer)
            
def reset_password():
    user_name = input("Enter user name to reset his password: ")
    client_socket.send(user_name.encode('utf8'))

def send_to_all():
    message_content = input("Your message: ")
    client_socket.send(message_content.encode('utf8'))
    print("Your message has been sent to all")

def read_for():
    read_for_user = input("Enter the username to read his messages: ")
    client_socket.send(read_for_user.encode('utf8'))
    user_inbox = client_socket.recv(1024)
    user_inbox = json.loads(user_inbox)

    for key, value in user_inbox.items():
        print(f"{key} from [{value}]")

def delete_user():
    username = input("Enter the username to delete: ")
    client_socket.send(username.encode('utf8'))
    server_answer = client_socket.recv(1024)
    print(server_answer.decode('utf8'))

def create_account():    
    print("[CREATE YOUR ACCOUNT]")
    while True:
        name = input("Name: ")
        password = pwinput.pwinput(prompt='Password: ', mask='*')
        account_data = json.dumps({name: password})
        client_socket.send(bytes(account_data, encoding="utf8"))

        validation = client_socket.recv(1024)
        msg = validation.decode('utf8')
        if msg == "wrong":
            print("Username is already taken. Try again.")
        elif msg == "done":
            print("Account created successfully.")
            break

def log_in():
    print("[LOGIN YOUR ACCOUNT]")
    while True:
        name = input("Name: ")
        password = pwinput.pwinput(prompt='Password (if you want to reset your password type here \"reset\"): ', mask='*')
        login_data = json.dumps({name: password})
        client_socket.send(bytes(login_data, encoding="utf8"))
        if password == "reset":
            print("Your password reset request has been sent. After the admin reset your password, log on with \"newpassword\" and go to your inbox to set the new password")
            return
        validation = client_socket.recv(1024)
        msg = validation.decode('utf8')
        if msg == "wrong":
            print("Invalid username or password. Try again.")
        elif msg == "done":
            print("Logged in successfully.")
            break

def send_message():
    print("[SEND A MESSAGE]")
    recipient = input("Enter an username (if you want to send a message to the administrator type \"admin\"): ")
    message = input("Enter a message: ")
    message_data = json.dumps({recipient: message})
    client_socket.send(bytes(message_data, encoding="utf-8"))
    server_answer = client_socket.recv(1024)
    server_answer = server_answer.decode('utf8')
    if server_answer == "There is no such user" or server_answer == "You can't send a massage to yourself"\
    or server_answer == "The recipient's inbox is full, you cannot send the message":
        print(server_answer)
    else:
        print("Your message has been sent!")
    return

def read_message():
    print("[YOUR MAIL BOX]")
    message = client_socket.recv(1024)
    message_data = json.loads(message)
    reset_password = False
    for key, value in message_data.items():
        print(f"- \"{key}\"     |    {value}")
        if key == "type your new password":
            reset_password = True
    if reset_password == False:
        return
    else:
        new_password = pwinput.pwinput(prompt='Enter your new password: ', mask='*')
        client_socket.send(new_password.encode("utf-8"))
        return



HOST = socket.gethostbyname(socket.gethostname())
PORT = 31415

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST,PORT))
print(client_socket.recv(1024).decode("utf-8"))
while True:
    data = input("Enter the command: ").encode('utf-8')
    print()
    client_socket.send(data)
    msg = client_socket.recv(1024)
    if msg.decode('utf-8') == "Admin panel":
        admin_panel()
    elif msg.decode('utf-8') == "You have authenticated, you are given administrator privileges":
        print(msg.decode('utf-8'))
    elif msg.decode("utf-8") == "Create account":
        create_account()
    elif msg.decode("utf-8") == "Log in":
        log_in()
    elif msg.decode("utf-8") == "Send a message":
        send_message()
    elif msg.decode("utf-8") == "Read a message":
        read_message()
    elif msg.decode("utf-8") == "Your inbox is now empty":
        print(msg.decode("utf-8"))
    elif msg.decode("utf-8") == "Logged out":
        print("You have been logged out")
        continue
    elif msg.decode("utf8") == "Stop the client":
        print("Goodbye!")
        client_socket.close()
        break
    else:
        for key, value in json.loads(msg).items():
            print(f"{key}: {value}")
    print()
