# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from scrapy.exceptions import DropItem
from scrapy.conf import settings
from scrapy import log

# 管道这里是定义 存储数据的地方

class DoubanPipeline(object):

    def __init__(self):
        # 初始化属性下，建立mongodb数据库连接， 在settings.py中定义的数据库的参数，是这样使用的
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        # 建立数据库 douban
        db = connection[settings['MONGODB_DB']]
        # 建立集合 movie 在这里定义的是一个数据库对象， mongodb的属性都是使用collection表示的， 初始化对象的属性
        #  初始化就相当于给变量第一次赋值 初始化就是把变量赋为默认值，把控件设为默认状态，把没准备的准备
        #  格式化，就是把磁盘恢复到初始化的状态， 磁盘的初始化状态为空
        self.collection = db[settings['MONGODB_COLLECTION']]

    # 处理 item  item是个字典
    def process_item(self, item, spider):

        valid = True
        #  判断下item中是否有数据
        for data in item:
            if not data:
                valid = False
                # 引发这个错误 程序就停止执行了
                raise DropItem("Missing %s of blogpost from %s" % (data, item['url']))
        if valid:
            # 如果有数据 ，取出字典中数据
            # 爬虫中是使用yield生成的， 是一条一条生成的，这边也是一条一条插入的
            new_moive = [{
                "total": item['title'],
                "score": item['score'],
                "motto": item['motto']
            }]
            # 往 mongodb的集合中插入字典
            self.collection.insert(new_moive)
            log.msg("Item wrote to MongoDB database %s/%s" %
                    (settings['MONGODB_DB'], settings['MONGODB_COLLECTION']),
                    level=log.DEBUG, spider=spider)
        # 最后别忘了返回item
        return item
