import socket
import json
import pwinput

def create_account():
    print("[CREATE YOUR ACCOUNT]")
    validation = give_account_data("create")
    if validation == False:
        return
    if validation == True:
        print("Your account has been created")
        return

def log_in():
    print("[LOGIN YOUR ACCOUNT]")
    validation = give_account_data("login")
    if validation == False:
        return False
    if validation == True:
        print("Your account has been created")
        return True

def send_message():
    print("[SEND A MESSAGE]")
    recipient = input("Enter an username: ")
    message = input("Enter a message: ")
    message_data = json.dumps({recipient: message})
    client_socket.send(bytes(message_data, encoding="utf-8"))
    print("Your message has been sent!")

def read_message():
    print("[YOUR MAIL BOX]")
    message = client_socket.recv(1024)
    message_data = json.loads(message)
    for key, value in message_data.items():
        print(f"- \"{key}\"     |    {value}")

def give_account_data(mode):
    name = input("Name: ")
    password = pwinput.pwinput(prompt='Password: ', mask='*')
    account_data = json.dumps({name: password})
    client_socket.send(bytes(account_data, encoding="utf8"))
    validation = client_socket.recv(1024)
    msg = validation.decode('utf8')
    if msg == "wrong":
        if mode == "create":
            print("Username is already taken. Try again.")
        else:
            print("Login error, try again.")
        return False
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
    if msg.decode("utf-8") == "Create account":
        create_account()
    elif msg.decode("utf-8") == "Log in":
        log_in()
    elif msg.decode("utf-8") == "Send a message":
        send_message()
    elif msg.decode("utf-8") == "Read a message":
        read_message()
    elif msg.decode("utf8") == "Stop the client":
        print("Goodbye!")
        client_socket.close()
        break
    else:
        for key, value in json.loads(msg).items():
            print(f"{key}: {value}")
    print()
