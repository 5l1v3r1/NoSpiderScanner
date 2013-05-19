import pymongo
from myconfigparser import get_list


CONN = pymongo.Connection("localhost", 27017)
DB = CONN["reqs"]


