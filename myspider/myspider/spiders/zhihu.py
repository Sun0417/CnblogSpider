# -*- coding: utf-8 -*-
import scrapy
from  selenium import webdriver
import time
from mouse import move,click
from  scrapy import Request

import pickle


class ZhihuSpider(scrapy.Spider):
    name = 'zhihu'
    allowed_domains = ['www.zhihu.com']
    start_urls = ['https://www.zhihu.com/']



    def start_requests(self):


        # cookies = pickle.load(open("D:/python_project/regtest/myspider/myspider/cookies/zhihu.cookies",'rb'))
        # cookie = dict()
        # for c in cookies:
        #     cookie[c['name']] = c['value']
        # # 返回一个list的Request dont_filter关闭
        # # 利用cookis 应该去setting中配置
        # # 开启 COOKIES_ENABLED = True  返回Request就不需要加cookies了 后续会自动传过去
        # # DOWNLOADER_MIDDLEWARES = {
        # #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 2
        # # }
        # return [scrapy.Request(url=self.start_urls[0], dont_filter=True, cookies=cookie)]

        """
        拦截模拟登陆
        后台本地启动Chrome应用  防止服务器端拦截
        原因是：如果用webdriver的Chrome 服务器将会拦截，等不了
        :return:
        """
        from selenium.webdriver.chrome.options  import  Options
        from selenium.webdriver.common.keys import Keys
        # 实例化option
        chrome_option = Options()
        chrome_option.add_argument('--disable-extension')
        chrome_option.add_experimental_option('debuggerAddress','127.0.0.1:9222')

        browser = webdriver.Chrome(
            executable_path='D:/chromedriver_win32_2.34/chromedriver.exe',
            chrome_options=chrome_option)
        # browser.get('https://www.zhihu.com/signin')
        # # 鼠标的定位
        # move(915,334)
        # # 点击
        # click()
        # time.sleep(2)
        # # 用户名
        # browser.find_element_by_css_selector('.SignFlow-accountInput.Input-wrapper input')\
        #     .send_keys('13764882106')
        # # 密码
        # browser.find_element_by_css_selector('.SignFlow-password input')\
        #     .send_keys('******')
        # # 模拟点击登录
        # move(944,577)
        # click()
        # 通过登录后的页面获取cookies 我在这里没有改所以一直返回登录的html
        browser.get('https://www.zhihu.com/')
        # 获取cookies
        cookies = browser.get_cookies()
        # 序列化对象到文件中
        pickle.dump(cookies,open("D:/python_project/regtest/myspider/myspider/cookies/zhihu.cookies",'wb'))
        cookie = dict()
        for c in cookies:
            cookie[c['name']] = c['value']
        # 返回一个list的Request dont_filter关闭
        # 利用cookis 应该去setting中配置
        # 开启 COOKIES_ENABLED = True  返回Request就不需要加cookies了 后续会自动传过去
        # DOWNLOADER_MIDDLEWARES = {
        #     'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': 2
        # }
        return [scrapy.Request(url=self.start_urls[0],dont_filter=True,cookies=cookie)]

    def parse(self, response):
            pass
