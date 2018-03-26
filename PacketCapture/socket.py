import socket
import struct

socket = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x000x))

while True:
		packet = socket.recvfrom(4096)
		print(packet)
		break
