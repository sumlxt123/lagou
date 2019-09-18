#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


import scrapy
from ..items import ImagesrenameItem

class ImgsrenameSpider(scrapy.Spider):
    name = 'Imgs'
    allowed_domains = ['lab.scrapyd.cn']
    start_urls = [
        'http://lab.scrapyd.cn/archives/55.html',
        'http://lab.scrapyd.cn/archives/57.html'
    ]

    def parse(self, response):
        item = ImagesrenameItem()
        item['imgurl'] = response.css(".post img::attr(src)").extract()
        item['imgname'] = response.css(".post-title a::text").extract()
        yield item