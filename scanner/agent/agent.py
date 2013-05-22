import socket
import sys
import time
from tornado.log import gen_log
from ConfigParser import SafeConfigParser
import ast
import pymongo
import datetime

parser = SafeConfigParser()
parser.read("config.ini")
AGENTPORT = int(parser.get('Agent', 'port'))
MONGOIP = parser.get('Master', 'mongo_ip')
MONGOPORT = int(parser.get('Master', 'mongo_port'))
END_SYMBOL = parser.get('Protocol', 'end_symbol')
DBCONN = pymongo.Connection(MONGOIP, MONGOPORT)
REQ_DB = DBCONN.requests
TASKSINFO = DBCONN.tasksinfo


def recv_end(the_socket, End):
    total_data = []
    data = ''
    while True:
        data = the_socket.recv(8192)
        if End in data:
            total_data.append(data[:data.find(End)])
            break
        total_data.append(data)
        if len(total_data) > 1:
            # check if end_of_data was split
            last_pair = total_data[-2] + total_data[-1]
            if End in last_pair:
                total_data[-2] = last_pair[:last_pair.find(End)]
                total_data.pop()
                break
    return ''.join(total_data)


def recv_timeout(conn, timeout=0.5):
    conn.setblocking(0)
    total_data = []
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
            gen_log.info("recv_timeout failed")
    return ''.join(total_data)


def scan_task(data):
    """
    use objectid as taskid
    then insert it into taskinfo collections
    and the objectid would be returned by insert() function
    db = conn.tasksinfo
    db.collection_names()
    for task in db.tasksinfo.find():print task
    """
    req = ast.literal_eval(data)
    req_id = req['_id']
    task_id = TASKSINFO.tasksinfo.insert(
        {"req_id": req_id,
         "vul_num": -1,
         "resp": "",
         "start_time": datetime.datetime.utcnow()})
    print req['path'], task_id
    return str(task_id)


def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    agent_address = ('localhost', AGENTPORT)
    sock.bind(agent_address)
    sock.listen(1)

    while True:
        connection, master_address = sock.accept()
        try:
            task = recv_end(connection, END_SYMBOL)
            if task[0:1] == "0":
                task_id = scan_task(task[1:])
            connection.sendall(task_id)
        finally:
            connection.close()

if __name__ == "__main__":
    main()
