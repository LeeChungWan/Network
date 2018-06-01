import socket
import hashlib
import struct
import time

ip_address = '127.0.0.1'
port_number = 3333

DATA_MAX_SIZE = 1024


seqList = [0b0000, 0b0001, 0b0010, 0b0011, 0b0100, 0b0101, 0b0110, 0b0111]
seqIndex = 0

server_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_sock.bind((ip_address, port_number))
print("Server socket open...")

infoPacket,addr = server_sock.recvfrom(1045)
infoChecksum = infoPacket[:20]
infoSeqAndACK = infoPacket[20:21]
fileInfo = infoPacket[21:]

h = hashlib.sha1()
h.update(infoSeqAndACK + fileInfo)

#this case is not occured this week.
if infoChecksum != h.digest():
	print("No!")

seqNum = seqList[seqIndex] << 4
ACK = seqList[seqIndex]
seqIndex = (seqIndex + 1) % 8
seqAndACK = (seqNum|ACK).to_bytes(1, "big")

# send right seqAndACK.
server_sock.sendto(seqAndACK, addr)

print("Send file info ACK...")
total_size = struct.unpack("!i", fileInfo[:4])[0]
file_name = fileInfo[4:].decode()
path = "./received_dir/"+file_name
print("file Name = " + file_name)
print("file Size = " + str(total_size))
print("received file Path = " + path)

#file opne for write.
write_file = open(path, "wb")

#receiving data.
count = 0
current_size = 0
checkRecvACKIndex = 1
while current_size != total_size:
	h = hashlib.sha1()
	data_packet,addr = server_sock.recvfrom(1045)
	data_checksum = data_packet[:20]
	data_seq_num = data_packet[20:21]
	data_info = data_packet[21:]
	h.update(data_seq_num + data_info)
	
	recv_seq = data_seq_num.hex()[0:1]

	if count == 15:
		print("Wait for 5...")
		count += 1
		time.sleep(5)
	# checked checksum
	elif data_checksum == h.digest():
		# checked frame number. for discard nonportable packet.
		checkSeqNum = seqList[checkRecvACKIndex]<<4
		checkACK = seqList[checkRecvACKIndex]
		checkSeqAndACK = (checkSeqNum|checkACK).to_bytes(1, "big")
		# right packet		
		if data_seq_num == checkSeqAndACK: 
			count += 1
			checkRecvACKIndex = (checkRecvACKIndex + 1) % 8
			current_size += len(data_info)
			write_file.write(data_info)

			seqNum = seqList[seqIndex] << 4
			ACK = seqList[seqIndex]
			seqIndex = (seqIndex + 1) % 8
			seqAndACK = (seqNum|ACK).to_bytes(1, "big")

			# send right seqAndACK.
			server_sock.sendto(seqAndACK, addr)
		
			print("(corrent size / total size) = " + str(current_size) + "/" + str(total_size) + " , " + str(round(current_size/total_size*100, 3))+ "%")
		else:
			index = checkRecvACKIndex
			print("[Discard Packet] SEQ : " + str(recv_seq) + " ACK : " + str(recv_seq))
	else:
		# case NAK
		seqNum = seqList[seqIndex] << 4
		NAK = 0b1111
		seqAndNAK = (seqNum|NAK).to_bytes(1, "big")
		server_sock.sendto(seqAndACK, addr)
		print(" * Packet corrupted!! *** - Send To Sender NAK!")

print("End")
write_file.close()
