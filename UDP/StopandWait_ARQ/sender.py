import socket
import hashlib

receiverIP = '127.0.0.1'
receiverPort = 3333
DATA_MAX_SIZE = 1024

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_sock.settimeout(3)

seq_num = 0
NAK = 2

print("Sender Socket open...")
print("Receiver IP = " + receiverIP)
print("Receiver Port = " + str(receiverPort))
print("Send File Info(file Name, file Size, seqNum) to Server...")
file_name = "lol.png"
total_size = 0
current_size = 0
# during send file info, ouccured timeout.
while 1:
	try:
	# hash
		h = hashlib.sha1()
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
		break
	except socket.timeout as e:
		print("Time Out!!!")
		sender_sock.sendto(info_packet, (receiverIP, receiverPort))


read_file = open("./"+file_name, "rb")

#sending data.
while current_size != total_size:
	h = hashlib.sha1()
	data = read_file.read(1024)
	checksum = str(seq_num).encode() + data
	h.update(checksum)
	data_packet = h.digest() + str(seq_num).encode() + data
	sender_sock.sendto(data_packet, (receiverIP, receiverPort))
	#receive ACK
	ACK = sender_sock.recv(1)
	while ACK.decode() == str(NAK) :
		print(" * Received NAK - Retransmit!")
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		ACK = sender_sock.recv(1)
	if len(data) <1024 :
		current_size += len(data)
		print("(corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , 100.0%")
	else :
		current_size += 1024
		print("(corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
	

read_file.close()

