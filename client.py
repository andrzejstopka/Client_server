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
        elif server_answer == "off":
            return

        
            
def reset_password():
    user_name = input("Enter user name to reset his password: ")
    client_socket.send(user_name.encode('utf8'))

def create_account():    
       while True:
        print("[CREATE YOUR ACCOUNT]")
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
    while True:
        print("[LOGIN YOUR ACCOUNT]")
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
    elif msg.decode("utf-8") == "Create account":
        create_account()
    elif msg.decode("utf-8") == "Log in":
        log_in()
    elif msg.decode("utf-8") == "Send a message":
        send_message()
    elif msg.decode("utf-8") == "Read a message":
        read_message()
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
