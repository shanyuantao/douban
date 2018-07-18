# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

import pymongo
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline
from scrapy import log, Request
from scrapy.conf import settings

logger = logging.getLogger('SaveImagePipeline')


class SaveImagePipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield Request(url=item['url'])

    def item_completed(self, results, item, info):
        logging.debug('图片下载完成')
        if not results[0][0]:
            raise DropItem('下载失败')

        return item

    def file_path(self, request, response=None, info=None):
        return request.url.split('/')[-1]

#
# class SaveToMongoPipeline(object):
#
#     def __init__(self):
#         connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
#         # 建立数据库
#         db = connection[settings['MONGODB_DB']]
#         # 建立集合
#         self.collection = db[settings['MONGODB_COLLECTION']]
#
#     def process_item(self, item, spider):
#         valid = True
#         for data in item:
#             if not data:
#                 valid = False
#                 raise DropItem("Missing %s of blogpost from %s" % (data, item['url']))
#         if valid:
#             new_image = [{
#                 "title": item['title'],
#                 "tag": item['tag'],
#                 "width": item['width'],
#                 "height": item['height'],
#                 "url": item['url'],
#             }]
#             self.collection.insert(new_image)
#             log.msg("Item wrote to MongoDB database %s/%s" %
#                     (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
#                     level=log.DEBUG, spider=spider)
#         return item
