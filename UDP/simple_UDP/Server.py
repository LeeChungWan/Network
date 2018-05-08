import socket

ip_address = '127.0.0.1'
port_number = 3333

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")
print("------------------------------------------------------")
print("Listening...")
while True:
	data,addr = server_sock.recvfrom(5000)
	recvType = data.decode()[0:1]
	recvData = data.decode()[1:]
	print("Type of Message : " + data.decode()[0:1])
	print("Received Message from client : " + recvData)
	if recvType == "0":
		data = recvData.upper()
	elif recvType == "1":
		data = recvData.lower()
	elif recvType == "2":
		data = recvData.swapcase()
	elif recvType == "3":
		data = recvData[::-1]
	print("Converted Message : " + str(data))

	server_sock.sendto(data.encode(), addr)
	print("Send message to client back...")
	print("------------------------------------------------------")
	print("Listening...")



