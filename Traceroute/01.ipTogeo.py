import re
import sys
import subprocess
import pygeoip

def is_valid_ip(ip):
    m = re.match(r"^(\d{1,3})\.(\d{1,3})\.(\d{1,3})\.(\d{1,3})$", ip)
    return bool(m) and all(map(lambda n: 0 <= int(n) <= 255, m.groups()))


def check_input():
	if len(sys.argv) < 2:
		print("Input argument is one")
		sys.exit()
	print("[Destination] ", sys.argv[1])

def get_ip_list():
	ip_list = []
	with subprocess.Popen(["traceroute", sys.argv[1]], stdout=subprocess.PIPE) as proc:
		out, err = proc.communicate()
		decode = out.decode("utf-8")
		arr = decode.split("\n")
		for i in range(1, len(arr)):
			sub_list = arr[i].split()
			if len(sub_list) > 1 and sub_list[1] is not "*":
				ip_list.append(sub_list[1])
	return ip_list

def get_coordinates(ip_list):
	geo = pygeoip.GeoIP('GeoLiteCity.dat')
	for i in range(len(ip_list)):
		ip = ip_list[i]
		if is_valid_ip(ip):
			ip_info = geo.record_by_name(ip)
			if ip_info is not None:
				latitude, longitude = ip_info['latitude'], ip_info['longitude']
				print("[IP] ", ip, " - ", "Lat : ", latitude, ", Lon : ", longitude)
			else:
				print("[IP] ", ip, " - No Geolocation Info.")

def main():
	check_input()
	ip_list = get_ip_list()
	get_coordinates(ip_list)

if __name__ == '__main__':
	main()
