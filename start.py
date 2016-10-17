# -*- coding: utf-8 -*-
import os
import pymongo
from scrapy import cmdline
from proxyip.spiders.ipspider import IpspiderSpider
from scrapy.utils.project import get_project_settings
if __name__ == '__main__':
        settings = get_project_settings()
        client = pymongo.MongoClient(
                settings.get('MONGODB_SERVER'),
                settings.get('MONGODB_RORT')
                )
        client['proxyip-database'].authenticate(settings.get('MONGODB_USER'), settings.get('MONGODB_PWD'), settings.get('MONGODB_DB'), mechanism='MONGODB-CR')
        db = client[settings.get('MONGODB_DB')]
        collection = db[settings.get('MONGODB_COLLECTION')]
        if  collection.find().count() > 1000:
            print "more than 1000! see you next time~"
        else:
            print "ready to crawl~"
            cmdline.execute("scrapy crawl ipspider".split())
