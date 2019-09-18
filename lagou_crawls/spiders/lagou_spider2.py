#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware

import re
import sys
import logging
import scrapy
from ..items import LagouItem
from ..settings import LOG_LEVEL

logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
logger.setLevel(LOG_LEVEL)
format = logging.Formatter("%(asctime)s - %(filename)s [line:%(lineno)d] - %(levelname)s:\
 %(message)s")  # output format
sh = logging.StreamHandler(stream=sys.stdout)    # output to standard output
sh.setFormatter(format)
logger.addHandler(sh)


class LagouSpider(scrapy.Spider):
    # 爬虫的名字
    name = "lagou2"
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

        menu_name = response.xpath("//div[@class='menu_box']/div/div/h2/text()").extract_first().strip()

        """先按"""
        for item in response.xpath("//div[@class='menu_box']/div/dl/dd/a"):
            """实例化 items 并将获取的值放入到 infoitem 中"""
            infoitem = LagouItem()
            jobclass = item.xpath('text()').extract()
            joburl = item.xpath('@href').extract_first()

            infoitem['menu_name'] = menu_name
            infoitem['jobClass'] = jobclass
            infoitem['jobUrl'] = joburl

            logger.debug('infoitem jobClass: {}  joburl:{}  menu_name:{}'.format(infoitem['jobClass'],infoitem['jobUrl'],infoitem['menu_name']))

            """使用 yield 输出 infoitem"""
            # yield infoitem

            for i in range(30):
                """使用 yield 直接访问子 url"""
                joburl = joburl + str(i+1)
                try:
                    yield scrapy.Request(url=joburl, cookies=self.cookie,
                                         meta= {"jobClass":jobclass,"menu_name":menu_name} , callback=self.parse_url)
                except:
                    logger.error('yield error, plase loock lagou_spider in parse funcation.')
            pass


    def parse_url(self,response):

        jobclass = response.meta["jobClass"]
        menu_name = response.meta["menu_name"]


        for sel in response.xpath("//ul[@class='item_con_list']/li"):
            # 初始化
            Item = LagouItem()

            joburl = sel.xpath("div/div[@class='position']/div/a/@href").extract_first()
            jobname = sel.xpath("div/div/div/a/h3/text()").extract()
            if not joburl is None:
                Item['jobUrl'] = joburl
                Item['jobClass'] = jobclass
                Item['menu_name'] = menu_name

                Item['jobName'] = jobname

                logger.debug('parse_url  joburl value :{}   jobclass value :{}  jobname \
                value :{}'.format(joburl,jobclass,jobname))
                yield scrapy.Request(url=joburl,cookies=self.cookie,
                                     meta={"jobClass":jobclass,"jobUrl":joburl,"menu_name":menu_name},
                                     callback=self.parse_opation)
            else:
                pass


    def parse_opation(self,response):
        """
        获取每个职位页面的相关信息
        哪个公司招聘什么岗位
        岗位概述
        岗位详细描述
        薪酬
        """
        jobclass = response.meta["jobClass"]
        joburl = response.meta["jobUrl"]
        logger.debug('joburl value:{}'.format(joburl))
        logger.debug('joburl value:{}'.format(jobclass))
        # job_id = [re.sub('\D','', x ) for x in joburl]
        job_id = [re.sub('\D','', x) for x in joburl.split('/') if not re.sub('\D','', x) is '' ]
        logger.debug('job_id value:{}'.format(job_id))
        menu_name = response.meta["menu_name"]

        Item = LagouItem()
        jobcompany = response.xpath("//dl[@id='job_company']/dt/a/div/h2/text()").extract()
        jobcompanyurl = response.xpath("//div[@class='content_r']/dl/dt/a/@href").extract()
        jobname = response.xpath("//div[@class='job-name']/span/text()").extract()
        # 怎么高效处理含换行符的字符，是一个问题
        jobplace = "-".join(response.xpath("//div[@class='work_addr']/a/text()").extract()[:2]) + \
                   "".join(response.xpath("//div[@class='work_addr']/text()").extract()[2:]).replace('\n','').replace(' ','')
        jobplace = jobplace.replace('--','-')
        jobrequest = "".join(response.xpath("//dd[@class='job_request']/p/span/text()").extract()).replace(' ','')
        jobrequest = [x.strip() for x in jobrequest.split("/")]
        job_payment = jobrequest[0]
        job_place = jobrequest[1]
        job_experience = jobrequest[2]
        job_ed = jobrequest[3]

        jobpubish = response.xpath("//p[@class='publish_time']/text()").extract()
        jobadvatage = response.xpath("//dd[@class='job-advantage']/p/text()").extract()
        jobdescription = response.xpath("//dd[@class='job_bt']/div/p/text()").extract()

        job_scr = self.get_job_scription(jobdescription)

        # job_scr = {'job_id':job_id,'job_scr':job_scr}
        job_scr = [x.upper() for x in job_scr]
        # logger.debug('job_tmp value:{}'.format(job_scr))
        compansnum = response.xpath("//div[@class='item_container']/div[@class='item_content']/ul/li[@class='number']/span/text()").extract()
        logger.debug('compansnum before value:{}'.format(compansnum))
        if not compansnum is None:
            # compansnum = response.xpath("//div[@class='content_r']/dl/dd/ul/li[4]/text()").extract()
            compansnum = response.xpath("//div[@class='content_r']/dl/dd/ul/li/i[@class='icon-glyph-figure']/../text()").extract()
            compansnum = [x.strip() for x in compansnum if not x.strip() is '']
            logger.debug('compansnum if in value:{}'.format(compansnum))
        else:
            compansnum = [x.strip() for x in compansnum if not x.strip() is '']
            logger.debug('compansnum else in value:{}'.format(compansnum))

        # add position label
        positionlabel = response.xpath("//ul[@class='position-label clearfix']/li/text()").extract()
        positionlabel = [ x.strip() for x in positionlabel if not x is None]
        Item['menu_name'] = menu_name
        Item['job_place'] = job_place
        Item['jobClass'] = jobclass[0]
        Item['jobUrl'] = joburl
        Item['job_id'] = job_id[0]
        Item['jobCompany'] = jobcompany[0].strip()
        Item['jobCompanyurl'] = jobcompanyurl[0]
        Item['jobName'] = jobname[0]
        Item['jobPlace'] = jobplace
        # Item['jobrequest'] = jobrequest
        Item['jobpubish'] = jobpubish[0]
        Item['jobadvatage'] = jobadvatage[0]
        Item['jobdescription'] = jobdescription
        Item['job_payment'] = job_payment
        Item['job_experience'] = job_experience.replace('经验','')
        Item['job_ed'] = job_ed.replace('及以上','').replace('学历','')
        Item['job_scr'] = job_scr
        Item['compansnum'] = compansnum[0]

        Item['positionlabel'] = positionlabel

        yield Item
        pass

    def get_job_scription(self,scr=''):
        """处理职位中要求的技术，目前以英文作为筛选条件"""
        job_scription = []
        pattern = r'[a-zA-Z]+'
        regex = re.compile(pattern)
        # job_scription = [job_scription.extend(regex.findall(x)) for x in scr]
        for i in scr:
            print(i)
            job_scription.extend(regex.findall(i))
        logger.debug('get_job_scription function in: {}'.format(job_scription))
        return [x for x in job_scription if not x is '']