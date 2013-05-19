import pymongo
from myconfigparser import get_list
from ConfigParser import SafeConfigParser

parser = SafeConfigParser()
parser.read("config.ini")
NUM2SEND = parser.get('master', 'num2send')
CONN = pymongo.Connection("localhost", 27017)
DB = CONN["reqs"]

def send_tasks(docs):
    for req in docs:
        req_id = req['_id']
        #use objectid as taskid
        #then insert it into taskinfo collections
        #and the objectid would be returned by insert() function
        task_id = DB.tasksinfo.insert("req_id": req_id, "vul_num": -1, "resp": "")

def main():
    docs = DB.requests.find({}).limit(NUM2SEND)
#do something here

    while(docs.hasNext()):
        more = docs.hasNext()
#do something with more


