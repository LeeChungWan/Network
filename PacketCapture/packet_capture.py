import socket
import struct
import re

recv_socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

def convertBytesToMacAddr(bytes_addr):
	mac_addr = ""
	splitedStr = re.findall('..', bytes_addr)
	
	for i in range(0, len(splitedStr)):
		mac_addr += splitedStr[i]
		if i < len(splitedStr) -1:
			mac_addr += ":"
	return mac_addr

while True:
	packet = recv_socket.recvfrom(4096)
	print(packet[0][0:14])

	ethernet_header = struct.unpack("!6s6s2s", packet[0][0:14])

	dst_ethernet_addr = ethernet_header[0].hex()
	src_ethernet_addr = ethernet_header[1].hex()
	protocol_type = "0x"+ethernet_header[2].hex()

	print("=====================================================")
	print("\tEthernet II")
	print("=====================================================")
	print("Destination MAC address : " + convertBytesToMacAddr(dst_ethernet_addr))
	print("Source MAC address : " + convertBytesToMacAddr(src_ethernet_addr))
	print("Type : " + protocol_type)
	
