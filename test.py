# encoding:utf-8

import requests, time, csv, os
from lxml import etree
from selenium import webdriver


class Music:
    # 初始化方法，定义变量
    def __init__(self):
        self.url = 'http://online.musicchina-expo.com/index/webshowindex'
        self.driver = webdriver.Chrome()
        self.driver.get(self.url)
        self.driver.maximize_window()
        time.sleep(1)
        self.driver.switch_to.frame('PreRegFrame')
        time.sleep(1)
        # self.driver.find_element_by_id('pageinput').send_keys('129')
        # self.driver.find_element_by_id('gotobtn').click()

    def Music_Url(self):
        file_path = os.path.join(os.getcwd(), 'messages.csv')
        f = open(file_path, 'a')
        for i in range(1):  # 页数
            try:
                for i in range(2, 32):
                    self.driver.find_element_by_xpath(
                        '//*[@id="f1"]/table/tbody/tr[3]/td/table/tbody/tr[' + str(i) + ']/td[4]/a').click()
                    time.sleep(0.3)
                    name = self.driver.find_element_by_xpath(
                        '/html/body/table/tbody/tr[1]/td/table/tbody/tr[2]/td[2]').text
                    phone = self.driver.find_element_by_xpath(
                        '/html/body/table/tbody/tr[1]/td/table/tbody/tr[7]/td[2]').text
                    f.write(','.join([name, phone, '\n']))
                    print(name, '   ', phone)
                    self.driver.find_element_by_xpath('/html/body/table/tbody/tr[4]/td/a').click()
                    time.sleep(0.3)
                self.driver.find_element_by_xpath(
                    '//*[@id="f1"]/table/tbody/tr[3]/td/table/tbody/tr[32]/td/table/tbody/tr/td[6]/a').click()
            except Exception as e:
                print(str(e))
        f.close()
        time.sleep(1)
        self.driver.switch_to.default_content()
        self.driver.quit()


if __name__ == '__main__':
    Music().Music_Url()
