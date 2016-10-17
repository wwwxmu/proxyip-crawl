# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging
import pymongo
import codecs
import json
import urllib2
from scrapy.exceptions import DropItem
from scrapy.conf import settings

class ProxyipPipeline(object):
    def __init__(self):
        self.file = codecs.open('./proxyip.json', 'w+', encoding="utf-8")
    def process_item(self, item, spider):
        line = json.dumps(dict(item),encoding="UTF-8", ensure_ascii = False)+ '\n'
        self.file.write(line)
        return item

class MongoDBPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(
                settings['MONGODB_SERVER'],
                settings['MONGODB_RORT']
                )
        self.client['proxyip-database'].authenticate(settings['MONGODB_USER'], settings['MONGODB_PWD'], settings['MONGODB_DB'], mechanism='MONGODB-CR')
        self.db = self.client[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        noempty = True
        valid = False
        for data in item:
            if not data:
                noempty = False
                raise DropItem('Missing {0}'.format(data))
        if noempty:
            valid = self.proxy_valid(item)
            if valid:
                if not self.collection.find_one({'ip':item['ip']}):
                    self.collection.insert(dict(item))
                    logging.info(item['ip'] + "added to MongoDB database!")
                    print item['ip']+ "added to MongoDB database!"
                else:
                    logging.info(item['ip'] + ': had been existed!')
                    print item['ip'] + ": had been existed!"
            else:
                logging.info(item['ip']+ ': can not be used!')
                print item['ip'] +': can not be used!'
        return item
    def proxy_valid(self, item):
        logging.info('valid ip: %s' %(item['ip']))
        print 'valid ip: %s ' %(item['ip'])
        user_agent = "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0)"
        header = {"User-Agent": user_agent}
        proxy={'http':item['ip']+':'+item['port']}
        proxy_support=urllib2.ProxyHandler(proxy)
        opener=urllib2.build_opener(proxy_support)
        urllib2.install_opener(opener)
        test_url="http://www.baidu.com"
        req=urllib2.Request(test_url,headers=header)
        try:
            resp=urllib2.urlopen(req,timeout=5)
            if resp.code==200:
                return True
            else:
                return False
        except:
            return False
