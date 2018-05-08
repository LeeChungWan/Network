import socket
import hashlib

receiverIP = '127.0.0.1'
receiverPort = 3333
DATA_MAX_SIZE = 1024

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

seq_num = 0
# hash
h = hashlib.sha1()


print("Sender Socket open...")
print("Receiver IP = " + receiverIP)
print("Receiver Port = " + str(receiverPort))
print("Send File Info(file Name, file Size, seqNum) to Server...")
file_name = "lol.png"
read_file = open("./"+file_name, "rb")
total_size = len(read_file.read())
file_info = total_size.to_bytes(4, byteorder = "big") + file_name.encode()
checksum = str(seq_num).encode() + file_info
h.update(checksum)
info_packet = h.digest() + str(seq_num).encode() + file_info
sender_sock.sendto(info_packet, (receiverIP, receiverPort))
#receive ACK
ACK = sender_sock.recv(1)
while ACK.decode() != str((seq_num + 1) % 2) :
	sender_sock.sendto(info_packet, (receiverIP, receiverPort))
	ACK = sender_sock.recv(1)

print("Start File send")
# plus + 1 -> seq_num
seq_num = (seq_num + 1) % 2

read_file.close()
read_file = open("./"+file_name, "rb")

#sending data.
if total_size < 1024:
	data = read_file.read()
	checksum = str(seq_num).encode() + data
	h.update(checksum)
	data_packet = h.digest() + str(seq_num).encode() + data
	sender_sock.sendto(data_packet, (receiverIP, receiverPort))
	#receive ACK
	ACK = sender_sock.recv(1)
	while ACK.decode() != str((seq_num + 1) % 2) :
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		ACK = sender_sock.recv(1)
	print("(corrent size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
else:
	count = 0
	while 1:
		if total_size - (1024*count) >= 1024:
			data = read_file.read(1024)
			checksum = str(seq_num).encode() + data
			h.update(checksum)
			data_packet = h.digest() + str(seq_num).encode() + data
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			#receive ACK
			ACK = sender_sock.recv(1)
			while ACK.decode() != str((seq_num + 1) % 2) :
				sender_sock.sendto(data_packet, (receiverIP, receiverPort))
				ACK = sender_sock.recv(1)
			# plus + 1 -> seq_num
			seq_num = (seq_num + 1) % 2
			count = count + 1
			print("(current size / total size) = " + str(DATA_MAX_SIZE*count) + "/" + str(total_size) + " , " + str(round(DATA_MAX_SIZE*count/total_size*100, 3)) + "%")
		else:
			remain_data_size = total_size - (1024*count)
			data = read_file.read(remain_data_size)
			checksum = str(seq_num).encode() + data
			h.update(checksum)
			data_packet = h.digest() + str(seq_num).encode() + data
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			#receive ACK
			ACK = sender_sock.recv(1)
			while ACK.decode() != str((seq_num + 1) % 2) :
				sender_sock.sendto(data_packet, (receiverIP, receiverPort))
				ACK = sender_sock.recv(1)
			print("(current size / total size) = " + str(total_size) + "/" + str(total_size) + " , 100.0%")
			break
read_file.close()

