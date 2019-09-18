#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

import sys
import scrapy
from lagou.items import LagouItem
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
format = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s:\
 %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)


class LagouSpider(scrapy.Spider):
    # 爬虫的名字
    name = "lagou"
    # 允许爬取的域名列表
    allowed_domains = ["lagou.com"]
    # 起始的url列表
    start_urls = [
       "https://www.lagou.com"
    ]

    cookie = {
        'user_trace_token':'20170823200708-9624d434-87fb-11e7-8e7c-5254005c3644',
        'LGUID':'20170823200708-9624dbfd-87fb-11e7-8e7c-5254005c3644 ',
        'index_location_city':'%E5%85%A8%E5%9B%BD',
        'JSESSIONID':'ABAAABAAAIAACBIB27A20589F52DDD944E69CC53E778FA9',
        'TG-TRACK-CODE':'index_code',
        'X_HTTP_TOKEN':'5c26ebb801b5138a9e3541efa53d578f',
        'SEARCH_ID':'739dffd93b144c799698d2940c53b6c1',
        '_gat':'1',
        'Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6':'1511162236,1511162245,1511162248,1511166955',
        'Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6':'1511166955',
        '_gid':'GA1.2.697960479.1511162230',
        '_ga':'GA1.2.845768630.1503490030',
        'LGSID':'20171120163554-d2b13687-cdcd-11e7-996a-5254005c3644',
        'PRE_UTM':'' ,
        'PRE_HOST':'www.baidu.com',
        'PRE_SITE':'https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D7awz0WxWjKxQwJ9xplXysE6LwOiAde1dreMKkGLhWzS%26wd%3D%26eqid%3D806a75ed0001a451000000035a128181',
        'PRE_LAND':'https%3A%2F%2Fwww.lagou.com%2F',
        'LGRID':'20171120163554-d2b13811-cdcd-11e7-996a-5254005c3644'
    }


    def parse(self,response):
        logger.debug("response.url: {}".format(response.url))

        """先按"""
        for item in response.xpath("//div[@class='menu_box']/div/dl/dd/a"):
            """实例化 items 并将获取的值放入到 infoitem 中"""
            infoitem = LagouItem()
            jobclass = item.xpath('text()').extract()
            joburl = item.xpath('@href').extract_first()

            infoitem['jobClass'] = jobclass
            infoitem['jobUrl'] = joburl

            logger.debug('infoitem jobClass: {}  joburl:{}'.format(infoitem['jobClass'],infoitem['jobUrl']))

            """使用 yield 输出 infoitem"""
            # yield infoitem

            for i in range(30):
                """使用 yield 直接访问子 url"""
                joburl = joburl + str(i+1)
                try:
                    yield scrapy.Request(url=joburl, cookies=self.cookie,
                                         meta= {"jobClass":jobclass} , callback=self.parse_url)
                except:
                    logger.error('yield error, plase loock lagou_spider in parse funcation.')
            pass


    def parse_url(self,response):

        jobclass = response.meta["jobClass"]


        for sel in response.xpath("//ul[@class='item_con_list']/li"):
            # 初始化
            Item = LagouItem()

            jobname = sel.xpath("div/div/div/a/h3/text()").extract()
            jobmoney = sel.xpath("div/div/div/div/span/text()").extract()
            jobneed = sel.xpath("div/div/div/div/text()").extract()
            jobneed = jobneed[2].strip()

            jobcompany = sel.xpath("div/div/div/a/text()").extract()
            jobcompany = jobcompany[3].strip()

            jobplace = sel.xpath("div/div/div/a/span/em/text()").extract()

            jobtype = sel.xpath("div/div/div/text()").extract()
            jobtype = jobtype[7].strip()

            jobspesk = sel.xpath("div[@class='list_item_bot']/div/text()").extract()
            jobspesk = jobspesk[-1].strip()

            Item['jobClass'] = jobclass

            Item['jobName'] = jobname
            Item['jobMoney'] = jobmoney
            Item['jobNeed'] = jobneed
            Item['jobCompany'] = jobcompany
            Item['jobPlace'] = jobplace
            Item['jobType'] = jobtype
            Item['jobSpesk'] = jobspesk


            yield Item
            pass

