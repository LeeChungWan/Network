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

		#received ACK
		ACK = sender_sock.recv(1)
		#received NAK		
		while ACK.decode() != str((seq_num + 1) % 2) :
			print(" * Received NAK - Retransmit file Info!")
			h = hashlib.sha1()
			checksum = str(seq_num).encode() + file_info
			h.update(chceksum)
			info_packet = h.digest() + str(seq_num).encode() + file_info
			sender_sock.sendto(info_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		#received wrong ACK		
		while ACK.decode() != str((seq_num + 1) % 2) :
			print(" * Received AKC - Retransmit file Info!")
			sender_sock.sendto(info_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)

		
		print("Start File send")
		# plus + 1 -> seq_num
		seq_num = (seq_num + 1) % 2
		read_file.close()
		break
	except socket.timeout as e:
		print(" * Time Out!! ***")
		print("Retransmission File Info...")
		sender_sock.sendto(info_packet, (receiverIP, receiverPort))
		#received ACK
		ACK = sender_sock.recv(1)
		#received NAK		
		while ACK.decode() != str((seq_num + 1) % 2) :
			print(" * Received NAK - Retransmit file Info!")
			h = hashlib.sha1()
			checksum = str(seq_num).encode() + file_info
			h.update(chceksum)
			info_packet = h.digest() + str(seq_num).encode() + file_info
			sender_sock.sendto(info_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		#received wrong ACK		
		while ACK.decode() != str((seq_num + 1) % 2) :
			print(" * Received AKC - Retransmit file Info!")
			sender_sock.sendto(info_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		seq_num = (seq_num + 1) % 2
		print("Start File send")
		# plus + 1 -> seq_num
		seq_num = (seq_num + 1) % 2
		read_file.close()
		break


read_file = open("./"+file_name, "rb")

#sending data.
count = 0
while current_size != total_size:
	try:
		count += 1
		h = hashlib.sha1()
		data = read_file.read(1024)
		checksum = str(seq_num).encode() + data
		# wrong checksum
		if count == 15:
			checksum = data
		h.update(checksum)
		data_packet = h.digest() + str(seq_num).encode() + data
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		#received ACK
		ACK = sender_sock.recv(1)
		#received NAK
		while ACK.decode() == str(NAK) :
			print(" * Received NAK - Retransmit!")
			print("Retransmission : (corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
			h = hashlib.sha1()
			checksum = str(seq_num).encode() + data
			h.update(checksum)
			data_packet = h.digest() + str(seq_num).encode() + data
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		#received wrong ACK		
		while ACK.decode() != str((seq_num + 1) % 2) :
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)

		seq_num = (seq_num + 1) % 2
		current_size += len(data)

		print("(corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
	except socket.timeout as e:
		print(" * Time Out!! ***")
		print("Retransmission : (corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
		sender_sock.sendto(data_packet, (receiverIP, receiverPort))
		ACK = sender_sock.recv(1)
		#received NAK
		while ACK.decode() == str(NAK) :
			print(" * Received NAK - Retransmit!")
			print("Retransmission : (corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
			h = hashlib.sha1()
			checksum = str(seq_num).encode() + data
			h.update(checksum)
			data_packet = h.digest() + str(seq_num).encode() + data
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		#received wrong ACK		
		while ACK.decode() != str((seq_num + 1) % 2) :
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			ACK = sender_sock.recv(1)
		current_size += len(data)
		seq_num = (seq_num + 1) % 2
	

read_file.close()
