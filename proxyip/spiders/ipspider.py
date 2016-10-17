# -*- coding: utf-8 -*-
import logging
from proxyip.items import ProxyipItem
from scrapy import Spider, Request
from scrapy.selector import Selector

class IpspiderSpider(Spider):
    name = "ipspider"
    allowed_domains = ["kuaidaili.com"]

    def start_requests(self):
        for page in range(1,300):
            yield Request('http://www.kuaidaili.com/free/inha/'+ str(page) +'/',
                meta= {
                    'site': 'kuaidaili',
                    'page': page},
                callback = self.parse)

    def parse(self, response):
        logging.debug('crawling : %s, page: %d, status:%d' %(response.meta['site'],response.meta['page'],response.status))
        if response.status == 200:
            item = ProxyipItem()
            table = response.xpath('//*[@id="list"]/table/tbody/tr')
            for index, tb in enumerate(table):
                if  u'高匿名' == tb.xpath('td[3]/text()').extract()[0] and u'HTTP' == tb.xpath('td[4]/text()').extract()[0]:
                    item['ip'] = tb.xpath('td[@data-title="IP"]/text()').extract()[0]
                    item['port'] = tb.xpath('td[@data-title="PORT"]/text()').extract()[0]
                    item['location'] = tb.xpath('td[5]/text()').extract()[0]
                    item['resTime'] = tb.xpath('td[6]/text()').extract()[0]
                    item['lastTime'] = tb.xpath('td[7]/text()').extract()[0]
                    yield item
