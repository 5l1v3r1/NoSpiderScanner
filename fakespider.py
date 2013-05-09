from threading import Thread
import socket
import sys

def proxy():
	pass

def main():
	if len(sys.argv) < 2:
		print "Usage: python fakespider.py <port>"
		return sys.stdout

	host = "" #blank for localhost
	port = int(sys.argv[1])

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.bind((host, port))
		s.listen(50)

	except socket.error, (value, message):
		if s:
			s.close()
		print "Could not open socket:", message
		sys.exit(1)

	while True:
		conn, client_addr = s.accept()
		t = Thread(target=proxy, args=(conn, client_addr))
		t.start()

	s.close()