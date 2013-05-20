import socket
import sys
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read("config.ini")
AGENTPORT = parser.get('Agents', 'port')

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
agent_address = ('localhost', AGENTPORT)
sock.bind(agent_address)
sock.listen(1)

while True:
    connection, master_address = sock.accept()
