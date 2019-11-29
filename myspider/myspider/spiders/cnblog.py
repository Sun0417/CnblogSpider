# -*- coding: utf-8 -*-
from urllib import parse
import re
import json


from ..until import common
from ..items import CnBlogSpiderItem
from ..items import BlogItemLoad

import scrapy
from scrapy import Request

class CnblogSpider(scrapy.Spider):
    name = 'cnblog'
    allowed_domains = ['news.cnblogs.com']
    start_urls = ['http://news.cnblogs.com/']
    '''
    爬去列表的数据
    '''
    def parse(self, response):
        # 爬去列表的数据
        post_nodes = response.xpath('//div[@id="news_list"]/div[@class="news_block"]')
        for post_node in post_nodes:
            img_url = post_node.css('.entry_summary '
                                    'a img::attr(src)').extract_first("")
            # 如果存在//
            if img_url.startswith('//'):
                img_url = 'https:' + img_url
            post_url = post_node.css('.news_entry a::attr(href)').extract_first("")
            # 同yield关键字把详情页的url返回 通过异步的爬去详情页数据
            # 注：列表循环完成后或异步调用parse_detail
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={'front_img_url':img_url}, callback=self.parse_detail)

        # 爬去下一页的数据 用yield返回出去结束爬去列表
        next_url = response.xpath('//div[@class="pager"]'
                                        '//a[contains(text(), "Next >")]/@href')\
                                            .extract_first("")
        # 抛出下一页url 回调交给parse方法在爬去列表
        yield Request(url=parse.urljoin(response.url, next_url),callback=self.parse)

    '''
    爬去详情页的数据
    '''
    def parse_detail(self, response):

        match_re = re.match(".*?(\d+)", response.url)
        if match_re:
            # 通过itemLoad来解决多字段提前的时候，代码多的问题
            item_loads = BlogItemLoad(CnBlogSpiderItem(), response=response)
            item_loads.add_css('title', '#news_title a::text')
            item_loads.add_css('content', '#news_content')
            item_loads.add_css('source', '#come_from a::text')
            item_loads.add_xpath('create_at', '//div[@id="news_info"]//*[@class="time"]/text()')
            item_loads.add_xpath('tags', '//div[@id="news_more_info"]/div[1]/a/text()')
            if response.meta.get('front_img_url', []):
               item_loads.add_value('front_img_url', response.meta.get('front_img_url', []))
            item_loads.add_value('url', response.url)
            content_id = match_re.group(1)

            # 点赞数
            post_url = parse.urljoin(response.url,
                                     '/NewsAjax/GetAjaxNewsInfo?contentId={}'
                                     .format(content_id))
            yield Request(url=post_url,
                          meta={'blog_item_load':item_loads,'url':response.url},
                          callback=self.parse_nums)

    '''
    获取点赞数和阅读数
    '''
    def parse_nums(self, response):

        blog_item_load = response.meta.get('blog_item_load','')
        url = response.meta.get('url', '')
        re = json.loads(response.text)

        comment_count = re['CommentCount']
        total_view = re['TotalView']
        digg_count = re['DiggCount']

        url_object_id = common.get_md5(url)
        blog_item_load.add_value('url_object_id', url_object_id)
        blog_item_load.add_value('comment_count',comment_count)
        blog_item_load.add_value('total_view',total_view)
        blog_item_load.add_value('digg_count', digg_count)

        cn_blog_item = blog_item_load.load_item()

        yield cn_blog_item