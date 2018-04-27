import socket

ip_address = '127.0.0.1'
port_number = 2345

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening...")
server_sock.listen()

client_sock,addr = server_sock.accept()
print("Connected with client")

data = client_sock.recv(5000)
print("Received Message from client : " + data.decode())

client_sock.send(data)
print("Send Message back to client")
