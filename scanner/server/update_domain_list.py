# since update the domain info everytime the request comming is expense
#just create a crontab task to update the domain every day.
#find the intersection of new hosts and old host, then insert the intersection

#db.tasksinfo.distinct('host')
#from datetime import datetime, timedelta
#yesterday = datetime.now() - timedelta(days=1)
#db.requests.find({"create_time":{"$gt":datetime.datetime(2013,5,20)}}).distinct("host")
#today_hosts = db.requests.find({"create_time":{"$gt":yesterday}}).distinct("host")
#old_hosts = db.hosts.distinct("hosts")
#new_hosts = intersect(today_hosts, old_hosts)
#if len(new_hosts)>0:for ...

def intersect(a, b):
    return list(set(a) & set(b))


