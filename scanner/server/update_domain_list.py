import pymongo
from ConfigParser import SafeConfigParser
from datetime import datetime, timedelta

parser = SafeConfigParser()
parser.read("config.ini")
MONGOIP = parser.get('Mongo', 'mongo_ip')
MONGOPORT = int(parser.get('Mongo', 'mongo_port'))

CONN= pymongo.Connection(MONGOIP, MONGOPORT)
DB = CONN["reqs"]
DB.domains.ensure_index('domain', unique=True, dropDups=True)

yesterday = datetime.now() - timedelta(days=1)
for domain in DB.requests.find({"create_time":{"$gt":yesterday}}).distinct("host"):
    DB.domains.insert({'domain':domain})

print 'Domain list:\n'
for domain in DB.domains.find():
    print domain
