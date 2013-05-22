import pymongo
import socket
import sys
from myconfigparser import get_list
from ConfigParser import SafeConfigParser
from tornado.log import gen_log

parser = SafeConfigParser()
parser.read("config.ini")
NUM2SEND = int(parser.get('Master', 'num2send'))
AGENTPORT = int(parser.get('Agent', 'port'))
END_SYMBOL = parser.get('Protocol', 'end_symbol')

CONN = pymongo.Connection("localhost", 27017)
DB = CONN["reqs"]


def get_agent_ip():
    return "127.0.0.1"


def single_scan(req):
    send_task("0" + str(req) + END_SYMBOL)


def send_task(data):
    """
    I think protobuf is too heavy for my case
    Defining an ad hoc protocol works better in this simple case.
    The format should be:MODE|message|END_SYMBOL
    MODE=0: Scaning a single http request
    MODE=1: Scaning all the http requests in the same domain
    END_SYMBOL: ^@^E!N__D
    For example: 0{...}^@^E!N__D
    """
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agent_ip = get_agent_ip()
    agent_address = (agent_ip, AGENTPORT)
    sock.connect(agent_address)
    try:
        sock.sendall(data)
        taskid = sock.recv(24)
        if len(taskid) != 24:
            gen_log.info("Receive data from agent failed,data: %s", data)
        sock.close()
        return taskid
    finally:
        sock.close()


def main():
    docs = DB.requests.find({})
    for doc in docs:
        print doc['path']
        doc.pop('create_time')
        single_scan(doc)

if __name__ == "__main__":
    main()
