# -*- coding: utf-8 -*-
from urllib import parse
import re
import json


from ..until import common
from ..items import CnBlogSpiderItem

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
        post_nodes = response.xpath('//div[@id="news_list"]/div[@class="news_block"]')[:1]
        for post_node in post_nodes:
            img_url = post_node.css('.entry_summary '
                                    'a img::attr(href)').extract_first("")
            post_url = post_node.css('.news_entry a::attr(href)').extract_first("")
            # 同yield关键字把详情页的url返回 通过异步的爬去详情页数据
            # 注：列表循环完成后或异步调用parse_detail
            yield Request(url=parse.urljoin(response.url, post_url),
                          meta={'front_img_url':img_url}, callback=self.parse_detail)

        # 爬去下一页的数据 用yield返回出去结束爬去列表
        # next_url = response.xpath('//div[@class="pager"]'
        #                                 '//a[contains(text(), "Next >")]/@href')\
        #                                     .extract_first("")
        # 抛出下一页url 回调交给parse方法在爬去列表
        #yield Request(url=parse.urljoin(response.url, next_url),callback=self.parse)

    '''
    爬去详情页的数据
    '''
    def parse_detail(self, response):
        match_re = re.match(".*?(\d+)",response.url)
        if match_re:

            title = response.css('#news_title a::text').extract_first("")
            create_at_re = response.xpath('//div[@id="news_info"]//*[@class="time"]/text()').extract_first("")
            match_re_create = re.match('.*?(\d+.*)',create_at_re)
            if match_re_create:
                create_at = match_re_create.group(1)
            content = response.css('#news_content').extract()[0]
            tag_list = response.xpath('//div[@id="news_more_info"]/div[1]/a/text()').extract()
            tags = ",".join(tag_list)
            source = response.css('#come_from a::text').extract_first("")
            content_id = match_re.group(1)
            post_url = parse.urljoin(response.url,
                                '/NewsAjax/GetAjaxNewsInfo?contentId={}'
                                .format(content_id))
            # 组织数据
            cn_blog_item = CnBlogSpiderItem()
            cn_blog_item['title'] = title
            cn_blog_item['create_at'] = create_at
            cn_blog_item['content'] = content
            cn_blog_item['tags'] = tags
            cn_blog_item['source'] = source
            cn_blog_item['front_img_url'] = response.meta.get('front_img_url','')
            # url md5 加密
            cn_blog_item['url'] = response.url
            cn_blog_item['url_object_id'] = common.get_md5(response.url)
            yield Request(url=post_url,
                          meta={'cn_blog_item':cn_blog_item},
                          callback=self.parse_nums)
            
        pass

    '''
    获取点赞数和阅读数
    '''
    def parse_nums(self, response):

        cn_blog_item = response.meta.get('cn_blog_item','')
        re = json.loads(response.text)
        comment_count = re['CommentCount']
        total_view = re['TotalView']
        digg_count = re['DiggCount']

        cn_blog_item['comment_count'] = comment_count
        cn_blog_item['total_view'] = total_view
        cn_blog_item['digg_count'] = digg_count

        yield cn_blog_item