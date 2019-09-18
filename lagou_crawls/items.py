# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    menu_name = scrapy.Field()
    jobClass = scrapy.Field()
    jobUrl = scrapy.Field()
    job_id = scrapy.Field()

    jobName = scrapy.Field()
    jobMoney = scrapy.Field()
    jobPlace = scrapy.Field()
    jobNeed = scrapy.Field()

    jobType = scrapy.Field()
    jobSpesk = scrapy.Field()

    jobrequest = scrapy.Field()
    jobpubish = scrapy.Field()
    jobadvatage = scrapy.Field()
    jobdescription = scrapy.Field()

    jobCompany = scrapy.Field()
    jobCompanyurl = scrapy.Field()
    compansnum = scrapy.Field()

    job_payment = scrapy.Field()
    job_experience = scrapy.Field()
    job_ed = scrapy.Field()
    job_place = scrapy.Field()
    job_scr = scrapy.Field()
    positionlabel = scrapy.Field()

    pass



class ImagesrenameItem(scrapy.Item):
    imgurl = scrapy.Field()
    imgname = scrapy.Field()
    image_paths = scrapy.Field()
    pass
