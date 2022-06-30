from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import re
import time
from scrapy import Selector
from models import *
import requests
def jd_evaluate(url):
    web = Chrome()
    web.get(url=url)
    web.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(5)
    sel=Selector(text=web.page_source)
    info=sel.xpath('//*[@id="comment-0"]/div[1]/div[2]/div[5]/div[1]/span')
    good_info=[]
    for inf in info:
        a="".join(inf.xpath('./text()').extract()).strip()
        good_info.append(a)
    good_info = good_info[:2]
    print(good_info)
if __name__ == '__main__':
    url="https://item.jd.com/100014348492.html"
    # jd_good(url)
    jd_evaluate(url)