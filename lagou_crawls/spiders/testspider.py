#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

import sys
import logging
import scrapy

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s:\
 %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)



class TestSpider(scrapy.Spider):
    # 爬虫的名字
    name = "testspider"
    # 允许爬取的域名列表
    allowed_domains = ["httpbin.com"]


    def start_requests(self):

        url = 'http://ip.chinaz.com/getip.aspx'

        yield scrapy.Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self,response):
        print(response.text)