# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import sys
import logging
from .settings import LOG_LEVEL

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(LOG_LEVEL)
format = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s:\
 %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)


class LagouPipeline(object):
    def process_item(self, item, spider):
        return item

"""
1、自定义 Pipeline 存储 JSon 数据
"""
import json
import codecs


class JsonWriterPipeline(object):
    def __init__(self):
        self.file = codecs.open('pipelinejson.json','w',encoding='utf-8')


    def process_item(self, item, spider):
        lines = json.dumps(dict(item),ensure_ascii=False) + '\n'
        self.file.write(lines)
        return item

    def close_spider(self,spider):
        self.file.close()


"""
2、使用 Scrapy 提供的 exporter 存储 JSon 数据
"""

from scrapy.exporters import JsonItemExporter


class JsonItemExporterPipeline(object):
    # 调用 scrapy 提供的 json exporter 导出 json 文件
    def __init__(self):
        self.file = open('pipelinejson_exporter.json','wb')
        # 初始化 exporter 实例，执行输出的文件和编码
        self.exporter = JsonItemExporter(self.file,encoding='utf-8',ensure_ascii=False)
        # 开启倒数
        self.exporter.start_exporting()

    def close_spider(self,spider):
        self.exporter.finish_exporting()
        self.file.close()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item



"""
3、使用 mongodb 数据库 存储数据
"""

import pymongo


class LagouMongoPipeline(object):
    # 定义 mongodb 数据库中集合名
    collection = 'lagoudata'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        """使用 settings.get 方法从配置文件中获取数据库配置信息"""
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        """
        spider start , before run the funcation, connt mongodb .
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item




class Lagou2MongoPipeline(object):
    # 定义 mongodb 数据库中集合名
    collection = 'lagoudata2'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,crawler):
        """使用 settings.get 方法从配置文件中获取数据库配置信息"""
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )

    def open_spider(self,spider):
        """
        spider start , before run the funcation, connt mongodb .
        :param spider:
        :return:
        """
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self,spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection].insert_one(dict(item))
        return item




"""
4、使用 MySQL 数据库 同步 存储数据 
"""

import pymysql
from pymysql.err import MySQLError

class MysqlPipeline(object):
    """使用同步方式向MySQL数据库存储数据"""
    def __init__(self,user,passwd,host,port,db,charset):
        self.user = user
        self.passwd = passwd
        self.host = host
        self.port = port
        self.db = db
        self.charset = charset

    @classmethod
    def from_crawler(cls,crawler):
        return cls(
            user=crawler.settings.get('MSQLUSER'),
            passwd=crawler.settings.get('MSQLPASSWD'),
            host=crawler.settings.get('MSQLHOST'),
            port=crawler.settings.get('MSQLPORT'),
            db=crawler.settings.get('MSQLDB'),
            charset=crawler.settings.get('MSQLCHARSET')
        )

    def open_spider(self,spider):
        """当数据库打开时创建数据库连接及游标对象"""
        self.client = pymysql.connect(host=self.host, port=self.port, user=self.user, passwd=self.passwd,\
                                      db=self.db, charset=self.charset)
        logger.debug('open_sipder in self client: {}'.format(self.client))
        self.cur = self.client.cursor()
        logger.debug('open_sipder in self cur: {}'.format(self.cur))

    def close_spider(self,spider):
        """当爬虫结束时关闭游标和数据库连接对象"""
        self.cur.close()
        self.client.close()

    def process_item(self,item,spider):
        """实现将数据库存入数据库的过程"""
        sql = """
              insert into lagou(jobclass,jobname,jobmoney,jobplace,jobneed,jobcompany,jobtype,jobspesk)
               values (%s,%s,%s,%s,%s,%s,%s,%s)
              """
        # 对插入语句进行异常处理
        try:
            self.cur.execute(sql, (item.get('jobClass'), item.get('jobName'), item.get('jobMoney'), \
                                   item.get('jobPlace'), item.get('jobNeed'), item.get('jobCompany'), \
                                   item.get('jobType'),item.get('jobSpesk')))
            self.client.commit()
        except MySQLError as e:
            logger.debug('db_insert except in err messages: {}'.format(e))
            self.client.rollback()
        return item









"""
5、使用 MySQL 数据库 twisted 异步 存储数据 
"""

from twisted.enterprise import adbapi


class MysqlTwistedPipelines(object):
    """基于 twisted。enterprise.adbapi 的异步 MySQL管道"""
    def __init__(self,dbpool):
        # self.user = user
        # self.passwd = passwd
        # self.host = host
        # self.port = port
        # self.db = db
        # self.charset = charset
        self.dbpool = dbpool

    @classmethod
    def from_crawler(cls,crawler):
        dbparms = dict(
            user=crawler.settings.get('MSQLUSER'),
            passwd=crawler.settings.get('MSQLPASSWD'),
            host=crawler.settings.get('MSQLHOST'),
            port=crawler.settings.get('MSQLPORT'),
            db=crawler.settings.get('MSQLDB'),
            charset=crawler.settings.get('MSQLCHARSET')
        )
        dbpool = adbapi.ConnectionPool("pymysql", **dbparms)
        return cls(dbpool)

    def process_item(self,item,spider):
        # 使用 twisted 将MySQL插入编程异步执行
        # 第一个参数是自己定义的函数，其中实现插入过程
        query = self.dbpool.runInteraction(self.db_insert,item)
        # 错误处理
        query.addErrback(self.handle_error)

    def handle_error(self,falure):
        """错误处理函数"""
        print(falure)

    def db_insert(self, cursor, item):
        """自定义插入语句，但这样有个问题，如果插入表的结构变化，则需要手工调整"""
        # 使用构造参数防止sql注入，其机制是内部对特殊字符进行转义，如 ' -> \'
        sql = """
              insert into lagou(jobclass,jobname,jobmoney,jobplace,jobneed,jobcompany,jobtype,jobspesk)
               values (%s,%s,%s,%s,%s,%s,%s,%s)
              """
        logger.debug('db_insert in sql: {}'.format(sql))
        try:
            logger.debug('db_insert add params after sql: {}'.format(sql))
            cursor.execute(sql,(item.get('jobClass'),item.get('jobName'),item.get('jobMoney'),\
                                item.get('jobPlace'),item.get('jobNeed'),item.get('jobCompany'),\
                                item.get('jobType'),item.get('jobSpesk')))
        except MySQLError as e:
            # except MySQLError:
            logger.debug('db_insert except in err messages: {}'.format(e))




"""
下载图片
"""

import re
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem

class ImagersrenamePipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        """循环每一张图片地址下载，若传过来的不是集合则无需循环直接 yield"""
        for image_url in item['imgurl']:
            logger.debug('image_url value:{}'.format(image_url))
            yield Request(image_url,meta={'name':item['imgname']})

    def file_path(self, request, response=None, info=None):
        """重命名 ，若不重写， 图片名为哈希 """
        # 提取url中的编号作为图片名
        image_guid = request.url.split('/')[-1]
        # 注意传过来的值的类型，有时因为类型不正确，也不会有正确返回结果，因而异常处理时非常有必要的
        name = request.meta['name'][0]
        logger.debug('name type value:{}'.format(type(name)))
        logger.debug('name value:{}'.format(name))
        name = re.sub(r'[？\\*|“<>:/]','',name)
        logger.debug('name re value:{}'.format(name))
        # 份文件夹存储的关键
        filename = u'{0}/{1}'.format(name,image_guid)
        logger.debug('filename value:{}'.format(filename))
        return filename

    def item_completed(self, results, item, info):
        """实现下载过程"""
        image_paths = [x['path'] for ok, x in results if ok]
        logger.debug('image_paths value: {}'.format(image_paths))
        if not image_paths:
            raise DropItem("Item contains non images.")
        item['image_paths'] = image_paths
        return item



