import pymongo
import socket
import sys
from myconfigparser import get_list
from ConfigParser import SafeConfigParser
from tornado.log import gen_log

parser = SafeConfigParser()
parser.read("config.ini")
NUM2SEND = int(parser.get('master', 'num2send'))
AGENTPORT = int(parser.get('Agents', 'port'))

CONN = pymongo.Connection("localhost", 27017)
DB = CONN["reqs"]


def get_agent_ip():
    return "127.0.0.1"


def single_scan(tasks):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agent_ip = get_agent_ip()
    agent_address = (agent_ip, AGENTPORT)
    sock.connect(agent_address)
    try:
        message = str(tasks)
        sock.sendall(message)
        taskid = sock.recv(24)
        if len(taskid) != 24:
            gen_log.info("Receive data from agent failed,data: %s", data)
        return taskid
    finally:
        sock.close()


def main():
    docs = DB.requests.find({})
    for doc in docs:
        print doc['path']
        single_scan(doc)
#    docs = DB.requests.find({}).limit(NUM2SEND)
#    for doc in docs:
#        print doc['path']
#        single_scan(doc)
#    while(docs.hasNext()):
#        more = docs.hasNext()
# do something with more

if __name__ == "__main__":
    main()
