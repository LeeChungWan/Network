import socket
import struct

sock = socket.socket(socket.AF_PACKET, socket.SOCK_RAW, socket.ntohs(0x0003))

while True:
		packet = socket.recvfrom(4096)
		print(packet)
		break
