import socket
import hashlib


receiverIP = '127.0.0.1'
receiverPort = 3333
DATA_MAX_SIZE = 1024

sender_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sender_sock.settimeout(3)

seqList = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
seqIndex = 0

# window's max size is 4.
window = [] 

print("Sender Socket open...")
print("Receiver IP = " + receiverIP)
print("Receiver Port = " + str(receiverPort))
print("Send File Info(file Name, file Size, seqNum) to Server...")
file_name = "dog.jpg"
total_size = 0
current_size = 0
current_window_data_size = []

checkRecvACKIndex = 0

# file read for file info.
read_file = open("./"+file_name, "rb")
total_size = len(read_file.read())
read_file.close()

# append file info to window list.
h = hashlib.sha1()
file_info = total_size.to_bytes(4, byteorder = "big") + file_name.encode()
seqNum = seqList[seqIndex]<<4
ACK = seqList[seqIndex]
seqIndex = (seqIndex + 1) % 8
seqAndACK = (seqNum|ACK).to_bytes(1, "big")
checksum = seqAndACK + file_info
h.update(checksum)
info_packet = h.digest() + seqAndACK + file_info
window.append(info_packet)

# file open for sending file data.
read_file = open("./"+file_name, "rb")

# numOfFrame add file info so count is -1 , not 0.
count = -1
while current_size != total_size:
	try:

		if count == -1:
			sender_sock.sendto(window[0], (receiverIP, receiverPort))
			current_window_data_size.append(total_size)
			count+=1
			
			
		# append file data until full window.			
		while len(window) != 4:
			h = hashlib.sha1()
			data = read_file.read(1024)
			if len(data) == 0:
				break
			seqNum = seqList[seqIndex]<<4
			ACK = seqList[seqIndex]
			seqAndACK = (seqNum|ACK).to_bytes(1, "big")
			checksum = seqAndACK + data
			h.update(checksum)
			data_packet = h.digest() + seqAndACK + data
			window.append(data_packet)
			if count == 5:
				h = hashlib.sha1()
				seqNum = seqList[seqIndex]<<4
				ACK = seqList[seqIndex]
				seqAndACK = (seqNum|ACK).to_bytes(1, "big")
				#wrong checksum				
				checksum = data
				h.update(checksum)
				wrong_data_packet = h.digest() + seqAndACK + data
				sender_sock.sendto(wrong_data_packet, (receiverIP, receiverPort))
			else:			
				# sending window's data to receiver.
				sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			count += 1
			current_size += len(data)
			current_window_data_size.append(len(data))
			print("[SEQ:"+ str(seqIndex) +"]"+"(corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
			seqIndex = (seqIndex + 1) % 8

		# received seqAndACK
		recvSeqAndACK = sender_sock.recv(1)
		checkSeqNum = seqList[checkRecvACKIndex]<<4
		checkACK = seqList[checkRecvACKIndex]
		checkSeqAndACK = (checkSeqNum|checkACK).to_bytes(1, "big")
		if recvSeqAndACK == checkSeqAndACK:
			# remove first value in window		
			window[0:1] = []
			current_window_data_size[0:1] = []
			checkRecvACKIndex = (checkRecvACKIndex + 1) % 8
			
		# case NAK.	
		else:
			print(" * Received NAK - Retransmit!")
			retransmit_data_size = sum(i for i in current_window_data_size)
			current_size -= retransmit_data_size
			for i in range(len(current_window_data_size)):
				data_packet = window[i]
				sender_sock.sendto(data_packet, (receiverIP, receiverPort))
				current_size += current_window_data_size[i]
				print("Retransmission : (corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
			

	except socket.timeout as e:
		print("*** Time Out!! ***")
		retransmit_data_size = sum(i for i in current_window_data_size)
		current_size -= retransmit_data_size
		for i in range(len(current_window_data_size)):
			data_packet = window[i]
			sender_sock.sendto(data_packet, (receiverIP, receiverPort))
			current_size += current_window_data_size[i]
			print("Retransmission : (corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
			

print("End")
read_file.close()








