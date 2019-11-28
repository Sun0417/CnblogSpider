# -*- coding: utf-8 -*-
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter


import codecs
import  json
import MySQLdb
from twisted.enterprise import adbapi

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MyspiderPipeline(object):
    def process_item(self, item, spider):
        return item

# 保存数据到db
class SaveDataMysqlPipeline(object):
    # 建立连接
    def __init__(self):
        self.con = MySQLdb.connect('127.0.0.1',
                        'root', '123456',
                        'test',
                        charset='utf8',use_unicode=True)
        self.cursor = self.con.cursor()
    def process_item(self, item, spider):
        insert_sql='''
            insert into  cnblog_atricle(title,url,url_object_id,front_img_url,front_img_path,
            comment_count,total_view,digg_count,tags,source,content,create_at)
            values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        '''
        # 赋值数据
        params = list()
        params.append(item.get('title',''))
        params.append(item.get('url', ''))
        params.append(item.get('url_object_id', ''))
        front_img_url = ','.join(item.get('front_img_url', []))
        params.append(front_img_url)
        params.append(item.get('front_img_path', ''))
        params.append(item.get('comment_count', 0))
        params.append(item.get('total_view', 0))
        params.append(item.get('digg_count', 0))
        params.append(item.get('tags', ''))
        params.append(item.get('source', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_at', '1970-01-01'))
        # 插入
        self.cursor.execute(insert_sql, tuple(params))
        # 提交
        self.con.commit()

        return item


# 异步插入mysql的方法  异步插入式基础
# from twisted.enterprise import adbapi
class MysqlTwistedPipeline(object):
    # 如果重载一个方法来配置 db的信息 创建mysql异步连接池
    @classmethod
    def from_settings(cls, settings):
        from MySQLdb.cursors import DictCursor
        # 数据库信息
        db_params = dict(
            host=settings['MYSQL_HOST'],
            db=settings['MYSQL_DBNAME'],
            user=settings['MYSQL_USER'],
            passwd=settings['MYSQL_PASSWORD'],
            charset=settings['CHAR_SET'],
            cursorclass=DictCursor,
            use_unicode=True
        )
        #  建立连接异步池
        db_pool = adbapi.ConnectionPool('MySQLdb', **db_params)
        # 直接返回出去 在__init__接受
        return  cls(db_pool)
      # 初始化 runInteraction 第一个参数为代用方法名称
    def __init__(self, db_pool):
        #初始化异步
        self.db_pool = db_pool

    def process_item(self, item, spider):
        # 执行异步 runInteraction 有两个参数
        # 第一个参数是需要执行的插入逻辑
        # 第二个参数是传入的参数
        query = self.db_pool.runInteraction(self.do_insert,item, spider)
        # 定义错误信息
        query.addErrback(self.handle_error, item , spider)
        return item

    # addErrback执行这个方法的时候 自动 默认注入 failure
    def handle_error(self, failure, item , spider):
        print(failure)

    # runInteraction执行这个方法的时候会默认注入cursor
    # 后面才是你传入的参数
    def do_insert(self, cursors, item , spider):
        insert_sql = '''
                    insert into  cnblog_atricle(title,url,url_object_id,front_img_url,front_img_path,
                    comment_count,total_view,digg_count,tags,source,content,create_at)
                    values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                    ON DUPLICATE KEY UPDATE comment_count=VALUES(comment_count),
                    total_view=VALUES(total_view),digg_count=VALUES(digg_count),
                    tags=VALUES(tags),source=VALUES(source)
                '''
        # 赋值数据
        params = list()
        params.append(item.get('title', ''))
        params.append(item.get('url', ''))
        params.append(item.get('url_object_id', ''))
        front_img_url = ','.join(item.get('front_img_url', []))
        params.append(front_img_url)
        params.append(item.get('front_img_path', ''))
        params.append(item.get('comment_count', 0))
        params.append(item.get('total_view', 0))
        params.append(item.get('digg_count', 0))
        params.append(item.get('tags', ''))
        params.append(item.get('source', ''))
        params.append(item.get('content', ''))
        params.append(item.get('create_at', '1970-01-01'))

        cursors.execute(insert_sql,tuple(params))



# 定义文件写入的Pipeline
class JsonWithEncodePipeline(object):
     # 打开文件 需要初始化
     def __init__(self):
         # 初始化已经赋值要 self.file
         self.file = codecs.open('article.json', 'w', encoding='utf-8')
     # 这个方法名和参数不能修改
     def process_item(self, item, spider):
         # 将item转json  ensure_ascii一定要设置False
         json_text = json.dumps(dict(item),ensure_ascii=False) + "\n"
         #写入文件
         self.file.write(json_text)
         # 一定要返回 不然下个Pipeline的item就会是Null
         return item

      #关闭文流
     def spider_closed(self, spider):
         self.file.close()

# 使用scrapy内置的文件写入操作
# from scrapy.exporters import JsonItemExporter
class JsonExportPipeline(object):
    def __init__(self):
        # 打开文件 已二进制的文件流打开
        self.file = open('export.json','wb')
        # 使用JsonItemExporter 返回对象
        self.export = JsonItemExporter(self.file,
                                       encoding='utf-8',
                                       ensure_ascii=False)
        # 开启
        self.export.start_exporting()

    def process_item(self, item, spider):
        # 写入
        self.export.export_item(item)
        return item

    # 关闭
    def spider_close(self, spider):
        self.export.finish_exporting()

# 需要获取图片上传的路径 需要继承ImagePipeline中拦截方法
# from scrapy.pipelines.images import ImagesPipeline
# scrapy.pipelines.images.ImagesPipeline 这里已经继承
# 所以需要在 修改配置文件的ITEM_PIPELINES 修改自己定的CnBlogImagePipeline
# myspider.pipelines.CnBlogImagePipeline
class CnBlogImagePipeline(ImagesPipeline):
        # 重写拦截方法
        def item_completed(self, results, item, info):
            front_img_path = '';
            if 'front_img_url' in item and len(item['front_img_url'])>0:
                for k,v in results:
                    front_img_path = v['path']
            item['front_img_path'] = front_img_path
            # 一定要返回回去 ,不然就直接停掉了
            return item

