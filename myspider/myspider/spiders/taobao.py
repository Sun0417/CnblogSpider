# -*- coding: utf-8 -*-
from urllib import parse

import scrapy

class TaoBaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['www.taobao.com']
    start_urls = ['https://www.taobao.com/']
    '''
    爬去列表的数据
    '''
    def parse(self, response):

        pass
