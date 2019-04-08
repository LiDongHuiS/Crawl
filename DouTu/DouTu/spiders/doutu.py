# -*- coding: utf-8 -*-
import scrapy, os, requests
from ..items import DoutuItem


class DoutuSpider(scrapy.Spider):
    name = 'doutu'
    allowed_domains = ["doutula.com", "sinaimg.cn"]
    start_urls = ['https://www.doutula.com/photo/list/?page={}'.format(i) for i in range(1, 1001)]

    def parse(self, response):
        i = 0
        for content in response.xpath('//*[@id="pic-detail"]/div/div[3]/div[2]/ul/li/div/div/a'):
            i += 1
            item = DoutuItem()
            try:
                item['img_url'] = content.xpath('//img/@data-original').extract()[i]
                item['name'] = content.xpath('//p/text()').extract()[i]
            except Exception as e:
                print(str(e))
            yield item
