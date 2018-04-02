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
	if protocol_type == "0x0800" :
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
		
		start_num = header_length_ip_arr + 14 #UDP, TCP's start byte number.
		
		if protocol_ip_arr is 6:
			print("=====================================================")
			print("\tTCP")
			tcp_header = struct.unpack("!2s2s4s4s2s2s2s2s", packet[0][start_num:start_num+20])
			src_port_tcp = int(tcp_header[0].hex(), 16)
			dst_port_tcp = int(tcp_header[1].hex(), 16)
			seq_num_tcp = int(tcp_header[2].hex(), 16)
			ack_set_tcp = int(tcp_header[3].hex(), 16)
			option_tcp = int(tcp_header[4].hex(), 16)
			data_offset_tcp = option_tcp >> 12
			reserved_tcp = (option_tcp & 3584) >> 9
			ns_tcp = (option_tcp & 256) >> 8
			cwr_tcp = (option_tcp & 128) >> 7
			ece_tcp = (option_tcp & 64) >> 6
			urg_tcp = (option_tcp & 32) >> 5
			ack_tcp = (option_tcp & 16) >> 4
			psh_tcp = (option_tcp & 8) >> 3
			rst_tcp = (option_tcp & 4) >> 2
			syn_tcp = (option_tcp & 2) >> 1
			fin_tcp = (option_tcp & 1)
			window_size_tcp = int(tcp_header[5].hex(), 16)
			check_sum_tcp = int(tcp_header[6].hex(), 16)
			urgent_pointer_tcp = int(tcp_header[7].hex(), 16)
			print("Source Port : " + str(src_port_tcp))
			print("Destination Port : " + str(dst_port_tcp))
			print("Sequence Number : " + str(seq_num_tcp))
			print("Acknowledge Number : " + str(ack_set_tcp))
			print("Data offset : " + str(data_offset_tcp))
			print("Reserved : " + str(reserved_tcp))
			print("NS : " + str(ns_tcp))
			print("CWR : " + str(cwr_tcp))
			print("ECE : " + str(ece_tcp))
			print("URG : " + str(urg_tcp))
			print("ACK : " + str(ack_tcp))
			print("PSH : " + str(psh_tcp))
			print("RST : " + str(rst_tcp))
			print("SYN : " + str(syn_tcp))
			print("FIN : " + str(fin_tcp))
			print("Window Size : " + str(window_size_tcp))
			print("TCP checksum : " + str(check_sum_tcp))
			print("Urgent Pointer : " + str(urgent_pointer_tcp))
			print("=====================================================")
		elif protocol_ip_arr is 17:
			print("=====================================================")
			print("\tUDP")
			print("=====================================================")
			udp_header = struct.unpack("!2s2s2s2s", packet[0][start_num:start_num+8])		
			src_port_udp = int(udp_header[0].hex(), 16)
			dst_port_udp = int(udp_header[1].hex(), 16)
			length_udp = int(udp_header[2].hex(), 16)
			check_sum_udp = int(udp_header[3].hex(), 16)
			print("Source Port : " + str(src_port_udp))
			print("Destination Port : " + str(dst_port_udp))
			print("UDP Length : " + str(length_udp))
			print("UDP Checksum : " + str(check_sum_udp))

