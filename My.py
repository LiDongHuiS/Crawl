# encoding:utf-8

import requests
from lxml import etree
from bs4 import BeautifulSoup


class City:
    # 初始化方法，定义变量
    def __init__(self):
        self.url = 'http://www.tcmap.com.cn/'

    def City_Url(self):
        html = requests.get(self.url)
        html.encoding = 'gb2312'
        city_url = etree.HTML(html.text).xpath('//*[@class="ht"]/b/a/@href')
        for c in city_url:
            city_url = self.url + c
            self.Town_Street(city_url)

    def Town_Street(self, city_url):

        town_html = requests.get(city_url)
        town_html.encoding = town_html.apparent_encoding
        xp = etree.HTML(town_html.text).xpath
        city = xp('//*[@id="page_left"]/div[1]/a[2]/text()')[0]
        town = xp('//strong/a/text()')
        if city == '北京' or city == '天津' or city == '上海' or city == '重庆':
            city = city + '市'
        elif city == '澳门':
            city = city + '特别行政区'
        elif city == '甘肃省' or city == '浙江省' or city == '香港特别行政区':
            city = city
        else:
            city = city + '省'

        for i in range(2, len(town) + 2):
            town_html = xp('//tr[{i}]/td[1]/strong/a/text()'.format(i=i))[0]
            administrative_divisions = xp('//tr[{i}]/td[6]/a/text()'.format(i=i))
            # print(city+town_html)
            for administrative_division in administrative_divisions:
                print(city + town_html + administrative_division)


City().City_Url()

