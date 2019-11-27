# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass



class CnBlogSpiderItem(scrapy.Item):
    title = scrapy.Field()
    create_at = scrapy.Field()
    content = scrapy.Field()
    tags = scrapy.Field()
    source = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_img_url = scrapy.Field()
    front_img_path = scrapy.Field()
    comment_count = scrapy.Field()
    total_view = scrapy.Field()
    digg_count = scrapy.Field()
    pass
