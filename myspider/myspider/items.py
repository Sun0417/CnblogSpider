# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

from scrapy.loader import ItemLoader
from scrapy.loader.processors import Identity,TakeFirst,MapCompose,Join

from .until import common

class MyspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

# 因为itemLoad返回的都list 我们在需要的是str类型 所有需要重写itemLoad
# 需要继承itemLoad
class BlogItemLoad(ItemLoader):
    # 输出改类型 默认是Identity 需要改成TaskFirst
    # 所属的包 from scrapy.loader.processors
    default_output_processor = TakeFirst()



class CnBlogSpiderItem(scrapy.Item):
    title = scrapy.Field()
    #如果字段做处理需要导入一个包 input_processor = MapCompose(回调方法)
    #from scrapy.loader.processors  下面的MapCompose
    # 参数是一个回调方法
    create_at = scrapy.Field(
        input_processor = MapCompose(common.regular_get_data)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        output_processor = Join(separator=',')
    )
    source = scrapy.Field(
        output_processor=Join(separator=',')
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field(
        input_processor = MapCompose(common.get_md5)
    )
    front_img_url = scrapy.Field(
        output_processor=Identity(),
    )
    front_img_path = scrapy.Field()
    comment_count = scrapy.Field()
    total_view = scrapy.Field()
    digg_count = scrapy.Field()
    pass
