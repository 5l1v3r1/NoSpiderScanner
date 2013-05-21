import pymongo
conn = pymongo.Connection("localhost", 27017)
db = conn["reqs"]
db.requests.remove()

