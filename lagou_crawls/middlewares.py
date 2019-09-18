# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
# from .settings import USER_AGENT_LIST
# from fake_useragent import UserAgent

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



class LagouSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


from scrapy import signals


class RandomUserAgentMiddleware(UserAgentMiddleware):
    """
    随机生成 user agent 的方法：
    1、在 settings 文件中进行配置，不需要启用中间件【但可能存在不能每次都切换的目的，除非重新读取配置文件时】
    2、使用fake_useragent 库来生成随机的 user agent
    3、引用配置文件中配置的 user_agent_list 列表来随机获取 user agent
    """
    # def __init__(self,user_agent='Scrapy'):
    #     self.user_agent = user_agent

    # def process_request(self, request, spider):
    #     """
    #     方法二：
    #     使用 fake_useragent 库来生成随机的 UserAgent
    #     目前提示 找不到 此模块，但是我已经在环境中安装，且测试导入未报错，原因到底是什么呢
    #     """
    #     ua = UserAgent()
    #
    #     request.headers['User-Agent'] = ua.random
    #     logger.debug("request.headers['User-Agent']: {}".format(request.headers['User-Agent']))

    # def process_request(self, request, spider):
    #     """
    #     方法三：
    #     使用 settings 文件中的user_agent_list列表 来生成随机的 UserAgent
    #     """
    #     agent = random.choice(list(USER_AGENT_LIST))
    #
    #     request.headers['User-Agent'] = agent
    #     logger.debug("request.headers['User-Agent']: {}".format(request.headers['User-Agent']))

    def __init__(self,user_agent=''):
        """当使用 from_crawler 时，user_agent 必须负值，且不能赋值为 None"""
        self.user_agent = user_agent

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            user_agent=crawler.settings.get('USER_AGENT_LIST')
        )

    def process_request(self, request, spider):
        agent = random.choice(self.user_agent)
        request.headers['User-Agent'] = agent




"""
代理设置
"""


class ProxyMiddleare(object):
    def __init__(self,ip=''):
        self.ip = ip
        logger.debug('proxmiddleare in ip value:{}'.format(self.ip))

    @classmethod
    def from_crawler(cls , crawler):
        return cls(
            ip=crawler.settings.get('IPPOOL')
        )

    def process_request(self,request,spider):
        proxyip = random.choice(self.ip)
        logger.debug('Using Proxy ip: {}'.format(proxyip))
        request.meta['proxy'] = proxyip
