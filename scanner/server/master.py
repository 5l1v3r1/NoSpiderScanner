import pymongo
import socket
import sys
from myconfigparser import get_list
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read("config.ini")
NUM2SEND = parser.get('master', 'num2send')
AGENTPORT = parser.get('Agents', 'port')

CONN = pymongo.Connection("localhost", 27017)
DB = CONN["reqs"]


def get_agent_ip():
    pass


def send_tasks(tasks):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agent_ip = get_agent_ip()
    agent_address(agent_ip, AGENTPORT)
    sock.connect(agent_address)
    try:
        message = str(tasks)
        sock.sendall(message)
        data = sock.recv(10)
        if data != "0":
            # loggin tasks here
    finally:
        # error logging here sys.stderr
        sock.close()
    """
    for req in docs:
        req_id = req['_id']
        #use objectid as taskid
        #then insert it into taskinfo collections
        #and the objectid would be returned by insert() function
        task_id = DB.tasksinfo.insert("req_id": req_id, "vul_num": -1, "resp": "")

"""


def main():
    docs = DB.requests.find({}).limit(NUM2SEND)
    send_tasks(docs)
    while(docs.hasNext()):
        more = docs.hasNext()
# do something with more
