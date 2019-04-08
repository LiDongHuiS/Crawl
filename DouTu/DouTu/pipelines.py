# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import os, requests, scrapy
from scrapy.utils.misc import md5sum
from scrapy.pipelines.images import ImagesPipeline


class DoutuPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        try:
            yield scrapy.Request(url=item['img_url'], meta={'item': item})
        except Exception as e:
            print(str(e))

    def item_completed(self, results, item, info):
        print('results: ', results)
        return item

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        # 自定义图片名称
        filename = u'{0}{1}'.format(item['name'], item['img_url'][-4:])
        # print('filename: ', filename)
        return filename

    # 设置gif图片下载后为动态图
    def check_gif(self, image):
        if image.format is None:
            return True

    def persist_gif(self, key, data, info):
        root, ext = os.path.splitext(key)
        absolute_path = self.store._get_filesystem_path(key)
        self.store._mkdir(os.path.dirname(absolute_path), info)
        f = open(absolute_path, 'wb')  # use 'b' to write binary data.
        f.write(data)

    # 重写图片下载规则
    def image_downloaded(self, response, request, info):
        checksum = None
        for path, image, buf in self.get_images(response, request, info):
            if checksum is None:
                buf.seek(0)
                checksum = md5sum(buf)
            width, height = image.size
            if self.check_gif(image):
                self.persist_gif(path, response.body, info)
            else:
                self.store.persist_file(
                    path, buf, info,
                    meta={'width': width, 'height': height},
                    headers={'Content-Type': 'image/jpeg'})
        return checksum

