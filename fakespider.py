from threading import Thread
from time import time, sleep
import socket
import sys

RECV_BUFFER = 8192
DEBUG = True

def recv_timeout(socks, timeout = 2):
    socks.setblocking(0);
    total_data = []
    data = ''
    begin = time()
    while True:
        if total_data and time() - begin > timeout:
            break
        elif time() - begin > timeout * 2:
            break
        try:
            data = socks.recv(RECV_BUFFER)
            if data:
                total_data.append(data)
                begin = time()
            else:
                sleep(0.1)
        except:
            pass
    return ''.join(total_data)

def proxy(conn, client_addr):
    request = recv_timeout(conn)

    first_line = request.split('\r\n')[0]
    if (DEBUG):
        #print request
        print "first_line: ", first_line
    url = first_line.split(' ')[1]

#    if (DEBUG):
#        print first_line
#        print
#        print "URL: ", url
#        print

    http_pos = url.find("://")
    if (http_pos ==  -1):
        temp = url
    else:
        temp = url[(http_pos + 3):]

    port_pos = temp.find(":")
    host_pos = temp.find("/")
    if host_pos == -1:
        host_pos = len(temp)

    host = ""
    if (port_pos == -1 or host_pos < port_pos):
        port = 80
        host = temp[:host_pos]
    else:
        port = int((temp[(port_pos + 1):])[:host_pos - port_pos - 1])
        host = temp[:port_pos]

    print "Connect to:", host, port

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(request)

        data = recv_timeout(s)
        if len(data) > 0:
            conn.send(data)
        s.close()
        conn.close()
    except socket.error, (value, message):
        if s:
            s.close()
        if conn:
            conn.close()
        print "Runtime error:", message
        sys.exit(1)



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

    while 1:
        conn, client_addr = s.accept()
        t = Thread(target=proxy, args=(conn, client_addr))
        t.start()

    s.close()

if __name__ == "__main__":
    main()
