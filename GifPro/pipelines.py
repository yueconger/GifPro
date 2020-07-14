# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import hashlib

import pymysql
import scrapy
from PIL import Image
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.misc import md5sum

from GifPro.settings import IMAGES_STORE


class GifproPipeline(object):
    def process_item(self, item, spider):
        return item


class MyImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        # 此方法在发送下载请求前调用(此方法本身就是求发送下载请求的)
        for imgage_url in item['pics']:
            print('当前url', imgage_url)
            headers = {
                'Content-Type': 'image/jpg',
                'Accept-Ranges': 'bytes',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
            }
            yield scrapy.Request(url=imgage_url, headers=headers, meta={'item': item, 'url':imgage_url})

    def check_gif(self, image):
        if image.format is None:
            return True

    def persist_gif(self, key, data, info):
        root, ext = os.path.splitext(key)
        absolute_path = self.store._get_filesystem_path(key)
        self.store._mkdir(os.path.dirname(absolute_path), info)
        f = open(absolute_path, 'wb')  # use 'b' to write binary data.
        f.write(data)

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

    def file_path(self, request, response=None, info=None):
        # 此方法是在图片将要被存储时被调用,获取图片存储路径
        item = request.meta['item']
        url = request.meta['url']
        print('存储url', url)
        obj = hashlib.md5()
        obj.update(bytes(url, encoding='utf-8'))
        name = obj.hexdigest()
        images_store = IMAGES_STORE
        image_path = os.path.join(images_store, name + '.' + url.split('/')[-1].split('.')[-1])
        print('下载', image_path)
        return image_path

    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        item['image_paths'] = image_paths
        print('******', image_paths)
        return item


class MySQLPipeline(object):
    def __init__(self):
        self.client = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',  # user
            passwd='mysql',  # pass
            db='meme',  # db
            charset='utf8'
        )
        self.cur = self.client.cursor()

    def process_item(self, item, spider):
        print('当前item', item)
        sql = 'insert into pics(title,tag,name_md5,url) VALUES (%s,%s,%s,%s)'
        lis = (item['title'], item['tag'], str(item['image_paths']), str(item['pics']))
        print(lis)
        print('数据开始写入')
        self.cur.execute(sql, lis)
        self.client.commit()
        return item