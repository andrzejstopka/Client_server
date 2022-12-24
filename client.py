import socket
import json
import pwinput

def give_data():
    name = input("Name: ")
    password = pwinput.pwinput(prompt='Password: ', mask='*')
    account_data = json.dumps({name: password, name: password})
    client_socket.send(bytes(account_data, encoding="utf8"))

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
        print("[CREATE YOUR ACCOUNT]")
        give_data()
    elif msg.decode("utf-8") == "Log in":
        print("[LOGIN YOUR ACCOUNT]")
        give_data()
    elif msg.decode("utf8") == "Stop the client":
        print("Goodbye!")
        client_socket.close()
        break
    else:
        for key, value in json.loads(msg).items():
            print(f"{key}: {value}")
        print()
