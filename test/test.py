
from selenium import webdriver
from scrapy.selector import Selector

browser = webdriver.Chrome(executable_path='D:/chromedriver_win32_2.34/chromedriver.exe')

browser.get('https://www.zhihu.com/signin?next=%2F')

# se = Selector(text=browser.page_source)
#
# print(se.css('.tm-promo-price tm-price::text').extract_first(''))

browser.find_element_by_css_selector('.SignFlow-accountInputContainer input[name="username"]').send_keys('13764882106')
browser.find_element_by_css_selector('.SignFlow-password.SignFlowInput input[name="password"]').send_keys('123456')

browser.\
    find_element_by_class_name('.SignContainer-inner button.Button--primary')\
    .click()


pass