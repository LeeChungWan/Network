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
index = 0
while True:
	packet = recv_socket.recvfrom(4096)
	#print(packet[0][14:16])

	ethernet_header = struct.unpack("!6s6s2s", packet[0][0:14])
	ip_header = struct.unpack("!1s1s2s2s2s1s1s2s4s4s", packet[0][14:34])
	
	dst_ethernet_addr = ethernet_header[0].hex()
	src_ethernet_addr = ethernet_header[1].hex()
	protocol_type = "0x"+ethernet_header[2].hex()
	
	version_ip_arr = ip_header[0].hex()[0:1]
	header_length_ip_arr = int(ip_header[0].hex()[1:2], 16) * 4
	TOS_ip_arr = int(ip_header[1].hex(), 16)
	total_length_ip_arr = int(ip_header[2].hex(), 16)	
	identifier_ip_arr = int(ip_header[3].hex(), 16)
	flags_ip_arr = int(ip_header[4].hex()[0:1], 16)
	fragment_offset_ip_arr = int(ip_header[4].hex()[1:4], 16)
	time_to_live_ip_arr = int(ip_header[5].hex(), 16)
	protocol_ip_arr = int(ip_header[6].hex(), 16)
	header_checksum_ip_arr = int(ip_header[7].hex(), 16)
	src_ip_arr = ""+str(int(ip_header[8].hex()[0:2], 16))+"."+str(int(ip_header[8].hex()[2:4], 16))+"."+str(int(ip_header[8].hex()[4:6], 16))+"."+str(int(ip_header[8].hex()[6:8], 16))
	dst_ip_arr = ""+str(int(ip_header[9].hex()[0:2], 16))+"."+str(int(ip_header[9].hex()[2:4], 16))+"."+str(int(ip_header[9].hex()[4:6], 16))+"."+str(int(ip_header[9].hex()[6:8], 16))
	print("=====================================================")
	print("\tEthernet II")
	print("=====================================================")
	print("Destination MAC address : " + convertBytesToMacAddr(dst_ethernet_addr))
	print("Source MAC address : " + convertBytesToMacAddr(src_ethernet_addr))
	print("Type : " + protocol_type)
	
	print("=====================================================")
	print("\tIPv4")
	print("=====================================================")
	print("Version : " + version_ip_arr)
	print("Internet Header Length : " + str(header_length_ip_arr))
	print("TOS : " + str(TOS_ip_arr))
	print("Total Length : " + str(total_length_ip_arr))
	print("Indentification : " + str(identifier_ip_arr))
	print("Flags : " + str(flags_ip_arr))
	print("TTL : " + str(time_to_live_ip_arr))
	print("Protocal : " + str(protocol_ip_arr))
	print("Header Checksum : " + str(header_checksum_ip_arr))
	print("Source IP address : " + src_ip_arr)
	print("Destination IP address : " + dst_ip_arr)
	
