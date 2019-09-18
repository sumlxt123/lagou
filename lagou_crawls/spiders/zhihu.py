#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


import re
import json

import scrapy
from urllib import parse


class ZhihuSpider(scrapy.Spider):
    """
    爬虫模拟实现登录
    """
    name = 'zhihu'
    allowed_domain = ["www.zhihu.com"]
    start_urls = ['https://www.zhihu.com/']
    headers = {
        'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36",
    }

    def start_requests(self):
        """
        重写 start_requests 请求页面登录
        :return:
        """
        return [scrapy.Request('https://www.zhihu.com/signup?next=%2F',headers=self.headers,callback=self.login)]

    def login(self,response):
        """
        先通过正则获取到
        :param response:
        :return:
        """