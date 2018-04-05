import socket

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening...")
data,addr = server_sock.recvfrom(5000)
print("Received Message from client : " + data.decode())

server_sock.sendto(data, addr)
print("Send message to client back...")
