import socket

serverIP = '127.0.0.1'
serverPort = 2345

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt_sock.connect((serverIP, serverPort))
print("Connect to Server...")

client_msg = input("input your Message : ")
clnt_sock.send(client_msg.encode())
print("Send Message to Server...")
print("Received Message from Server : " + (clnt_sock.recv(1024)).decode('utf-8'))
