import socket
import json
import datetime

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


HOST = socket.gethostbyname(socket.gethostname())
PORT = 31415


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    server_socket.bind((HOST, PORT))
    server_socket.listen()
    print("Server listening on...")
    client_socket, address = server_socket.accept()
    start_time = datetime.datetime.now()
    print(f"Client connected from {address[0]}:{address[1]}")
    client_socket.send("Welcome to the server, type \"help\" to check all commands".encode("utf8"))
    while True:

        data = client_socket.recv(1024).decode('utf8')

        if data == "uptime":
            msg = uptime(start_time)
        elif data == "info":
            msg = info()
        elif data == "help":
            msg = help()
        elif data == "stop":
            client_socket.send("Stop the client".encode("utf8"))
            print("Server is turning off")
            server_socket.close()
            break
        else:
            print(f"Unknown command: {data}")
            continue
        if data != "stop":
            msg = json.dumps(msg)
            client_socket.send(bytes(msg, encoding="utf8"))




