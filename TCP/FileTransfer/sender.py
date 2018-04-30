import socket

serverIP = '127.0.0.1'
serverPort = 2347
DATA_MAX_SIZE = 1024

clnt_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clnt_sock.connect((serverIP, serverPort))
print("Connect to Server...")
print("Receiver IP = " + str(serverIP))
print("Receiver Port = " + str(serverPort))
file_name = input("Input File Name : ")

# file open for read.
read_file = open("./"+file_name, "rb")

# getting the file size.
data = read_file.read() # data is str type. -> read_file is empty...
print("File Size = " + str(len(data)))
read_file = open("./"+file_name, "rb")
# file_name str to bytes. if file_name size is not 11, make size to 11.
gap = 11 - len(file_name)
if gap is not 0 :
	file_name = " "*gap + file_name

packet_type_msg = "0"
packet_type_data = "1"
current_size = 0
total_size = len(data)


encode_file_size = len(data).to_bytes(4, byteorder = "big")
packet_header = packet_type_msg.encode() + file_name.encode() + encode_file_size
# sending file info.
clnt_sock.send(packet_header)

# sending data.
if total_size < 1024:
	packet_data = packet_header + read_file.read(total_size)
	clnt_sock.send(packet_data)
	print("(corrent size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
else :
	count = 0;
	while total_size - (1024*count) >= 1024:	
		packet_data = packet_header + read_file.read(1024)
		clnt_sock.send(packet_data)
		count = count + 1
		print("(corrent size / total size) = " + str(DATA_MAX_SIZE*count) + "/" + str(total_size) + " , " + str(round(DATA_MAX_SIZE*count/total_size*100, 3)) + "%")
	remain_data_size = total_size - (1024*count)
	packet_data = packet_header + read_file.read(remain_data_size)
	clnt_sock.send(packet_data)
	print("(corrent size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
print("File send end.")
read_file.close()

