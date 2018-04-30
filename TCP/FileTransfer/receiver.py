import socket
import struct

ip_address = '127.0.0.1'
port_number = 2347
path = "./newFile/"
PACKET_HEAD_SIZE = 16
DATA_MAX_SIZE = 1024
PACKET_SIZE = PACKET_HEAD_SIZE + DATA_MAX_SIZE

server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

print("Listening...")
server_sock.listen()

client_sock,addr = server_sock.accept()



# file info. 16bytes
file_info = client_sock.recv(PACKET_HEAD_SIZE)
current_size = 0
total_size = struct.unpack("!i", file_info[12:16])[0]

print("Packet Type = " + file_info[0:1].decode())
print("File Size = " + str(total_size))
# delete spacebar in file_name.
file_name = ""
for i in file_info[1:12].decode(): 
	if i is not " ":
		file_name += i
path += file_name
print("File Path = " + path)


# file open for write.
write_file = open(path, "wb")


# receiving data.
if total_size < DATA_MAX_SIZE:
	receive_data = client_sock.recv(PACKET_HEAD_SIZE+total_size)
	write_file.write(receive_data[PACKET_HEAD_SIZE:])
	print("(corrent size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
else:
	count = 0
	while total_size - (DATA_MAX_SIZE*count) >= DATA_MAX_SIZE:
		receive_data = client_sock.recv(PACKET_SIZE)
		write_file.write(receive_data[PACKET_HEAD_SIZE:])
		count = count + 1
		print("(corrent size / total size) = " + str(DATA_MAX_SIZE*count) + "/" + str(total_size) + " , " + str(round(DATA_MAX_SIZE*count/total_size*100, 3)) + "%")
	remain_data_size = total_size - (DATA_MAX_SIZE*count)
	receive_data = client_sock.recv(PACKET_HEAD_SIZE + remain_data_size)
	write_file.write(receive_data[PACKET_HEAD_SIZE:])
	print("(corrent size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")

print("File receive end.")
write_file.close()

