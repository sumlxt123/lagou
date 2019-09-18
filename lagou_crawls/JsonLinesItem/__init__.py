#!/usr/bin/env python
# -*-coding:utf-8-*-
# author:sware


from scrapy.exporters import JsonLinesItemExporter



class ChongXie(JsonLinesItemExporter):
    """
    重写json编码规则
    """
    def __init__(self, file, **Kwargs):
        super(ChongXie, self).__init__(file, ensure_ascii = None)

