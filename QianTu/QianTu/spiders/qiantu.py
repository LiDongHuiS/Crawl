# -*- coding: utf-8 -*-
import scrapy, time, requests
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from lxml import etree
from ..items import QiantuItem

file_path = ''


class NameSpider(scrapy.Spider):
    name = 'qiantu'
    allowed_domains = ['588cu.com']

    def start_requests(self):
        base_url = 'http://588ku.com/sucai/0-default-0-0-{0}-0-{1}/'
        list1 = ["dongmanrenwu", "fengjingmanhua", "chuantongwenhua", "tiyuyundong", "huihuashufa",
                 "beijingdiwen", "huabianhuawen", "biankuangxiangkuang", "ziranfengguang", "renwenjingguan",
                 "jianzhuyuanlin", "yeshengdongwu", "jiaqinjiaxu", "yulei", "shenghuoyongpin", "canyinmeishi",
                 "tiyuyongpin", "kexueyanjiu", "gongyeshengchan", "jiaotonggongju", "shangyechahua",
                 "shangwuchangjing", "qita", "baozhuangsheji", "zhaotiesheji", "huacesheji"]

        for keyword in list1:  # 拼接url
            global file_path
            file_path = keyword

            #TODO:尝试获取到最大页数，目前不可用
            # page_url = base_url.format(keyword, 1)
            # print('page_url: ', page_url)
            # HTML = scrapy.Request(page_url)
            # max_page = etree.HTML(HTML).xpath('/html/body/div[4]/div/div/div[3]/div/ul/li[8]/a/text()')
            # if max_page != []:
            #     max_page = int(max_page[0])
            # elif max_page == []:
            #     max_page = 1
            # print('max_page: ', max_page)

            for page in range(1, 100):
                full_url = base_url.format(keyword, page)
                yield scrapy.Request(full_url, self.parse)

    def parse(self, response):
        pic_list = response.xpath('/html/body/div[4]/div/div/div[1]/div')
        for i in pic_list:
            item = QiantuItem()
            item['src'] = 'http://' + i.xpath('div[1]/a/img/@data-original').extract_first()  # 图片地址
            item['path'] = file_path  # 图片分类
            yield item

