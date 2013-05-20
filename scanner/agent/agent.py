import socket
import sys
import time
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read("config.ini")
AGENTPORT = parser.get('Agents', 'port')

def recv_timeout(conn, timeout=2):
    conn.setblocking(0)
    total_data=[]
    data = ''
    begin = time.time()
    while True:
        if total_data and time.time() - begin > timeout:
            break
        elif time.time() - begin > timeout * 2:
            break
        try:
            data = conn.recv(8192)
            if data:
                total_data.append(data)
                begin = time.time()
            else:
                time.sleep(0.1)
        except:
            #logging except here
    return ''.join(total_data)

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agent_address = ('localhost', AGENTPORT)
    sock.bind(agent_address)
    sock.listen(1)

    while True:
        connection, master_address = sock.accept()
        try:
            task = recv_timeout(connection)
            scan_task(task)
        finally:
            connection.close()

