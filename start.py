# -*- coding: utf-8 -*-
# check if the number of available IP in the database are more than 1000 Periodically.
import os
import urllib2
import pymongo
from scrapy import cmdline
from proxyip.spiders.ipspider import IpspiderSpider
from scrapy.utils.project import get_project_settings

def proxy_valid(ip,port):
    '''Check if the proxy ip is available
       Args:
            ip:ip address get from mongodb
            port: port get form mongodb
       return:
            True or False
            True: ip can be used
            False: ip is failure
    '''
    user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header = {"User-Agent": user_agent}
    proxy={'http': ip + ':' + port}
    proxy_support=urllib2.ProxyHandler(proxy)
    opener=urllib2.build_opener(proxy_support)
    urllib2.install_opener(opener)
    test_url="http://www.baidu.com"
    req=urllib2.Request(test_url,headers=header)
    try:
        #timeout 设置为10，如果你不能忍受你的代理延时超过10，就修改timeout的数字
        resp=urllib2.urlopen(req,timeout=20)
        if resp.code==200:
            return True
        else:
            return False
    except:
        return False

if __name__ == '__main__':
    user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
    header = {"User-Agent": user_agent}
    settings = get_project_settings()
    client = pymongo.MongoClient(
            settings.get('MONGODB_SERVER'),
            settings.get('MONGODB_RORT')
            )
    client['proxyip-database'].authenticate(settings.get('MONGODB_USER'), settings.get('MONGODB_PWD'), settings.get('MONGODB_DB'), mechanism='MONGODB-CR')
    db = client[settings.get('MONGODB_DB')]
    collection = db[settings.get('MONGODB_COLLECTION')]
    for col in collection.find():
        valid = True
        ip = col['ip']
        port = col['port']
        valid = proxy_valid(ip,port)
        print ip + str(valid)
        if not valid:
            collection.remove({"ip": ip})
    if  collection.count() > 1000:
        print "more than 1000! see you next time~"
    else:
        print "ready to crawl~"
        cmdline.execute("scrapy crawl ipspider".split())
