import socket

serverIP = '127.0.0.1'
serverPort = 3333

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client_msg = input("Input your Message : ")
clnt_sock.sendto(client_msg.encode(), (serverIP, serverPort))
print("Send Message to Server...")
print("Received Message from Server : " + (clnt_sock.recv(1024)).decode())
