from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
from scrapy import Selector
from models import *
import requests
def deil(nums_temp):
    nums=int(re.search('\d+',nums_temp).group(0))
    if '万' in nums_temp:
        nums = nums*10000
    return nums
def jd_good(url):
    web = Chrome()
    web.get(url=url)
    time.sleep(1)
    id= re.search('\d+',url).group(0)
    time.sleep(1)
    name=web.find_element(By.XPATH,"/html/body/div[6]/div/div[2]/div[1]").text
    time.sleep(1)
    content=web.find_element(By.XPATH,'//*[@id="p-ad"]').text
    time.sleep(1)
    supplier=web.find_element(By.XPATH,'//*[@id="summary-service"]/span').text
    time.sleep(1)
    web.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[2]').click()
    time.sleep(1)
    ggbz=web.find_element(By.XPATH,'//*[@id="detail"]/div[2]/div[2]/div[1]').text
    time.sleep(1)
    sel=Selector(text=web.page_source)
    image_list=sel.xpath('//*[@id="spec-list"]/ul/li')
    src_list=[]
    for image in image_list:
        src="".join(image.xpath('./img/@src').extract()).strip()
        src_list.append(src)
    price="".join(sel.xpath('/html/body/div[6]/div/div[2]/div[4]/div/div[1]/div[2]/span[1]/span[2]/text()').extract()).strip()
    time.sleep(1)
    web.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(1)
    good_rate=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[1]/div[1]/div').text
    time.sleep(1)
    comments_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[1]/a/em').text
    comments_nums=deil(comments_nums)
    has_image_comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[2]/a/em').text
    has_image_comment_nums=deil(has_image_comment_nums)
    has_video_comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[3]/a/em').text
    has_video_comment_nums=deil(has_video_comment_nums)
    has_add_comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[4]/a/em').text
    has_add_comment_nums=deil(has_add_comment_nums)
    well_comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a/em').text
    well_comment_nums=deil(well_comment_nums)
    middle_comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[6]/a/em').text
    middle_comment_nums=deil(middle_comment_nums)
    bad_comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[7]/a/em').text
    bad_comment_nums=deil(bad_comment_nums)
    good=Good()
    good.id=id
    good.name=name
    good.content=content
    good.supplier=supplier
    good.ggbz=ggbz
    good.image_list=src_list
    good.price=price
    good.good_rate=good_rate
    good.comments_nums=comments_nums
    good.has_image_comment_nums=has_image_comment_nums
    good.has_video_comment_nums=has_video_comment_nums
    good.has_add_comment_nums=has_add_comment_nums
    good.well_comment_nums=well_comment_nums
    good.middle_comment_nums=middle_comment_nums
    good.bad_comment_nums=bad_comment_nums
    good.save(force_insert=True)
def jd_evaluate(url):
    web = Chrome()
    web.get(url=url)
    # web.find_element(By.XPATH,'//*[@id="ttbar-login"]/a[1]').click()
    # web.find_element(By.XPATH,'//*[@id="content"]/div[2]/div[1]/div/div[3]/a').click()
    # web.find_element(By.XPATH,'//*[@id="loginname"]').send_keys('a13170474504')
    # web.find_element(By.XPATH,'//*[@id="nloginpwd"]').send_keys('caijiahao1')
    # web.find_element(By.XPATH,'//*[@id="loginsubmit"]').click()
    time.sleep(10)
    good_id= re.search('\d+',url).group(0)
    web.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(3)
    id=good_id
    time.sleep(3)
    user_name=web.find_element(By.XPATH,'//*[@id="comment-0"]/div[1]/div[1]/div[1]').text
    time.sleep(3)
    info_1=web.find_element(By.XPATH,'//*[@id="comment-0"]/div[1]/div[2]/div[3]/div[1]/span[1]').text
    time.sleep(3)
    info_2=web.find_element(By.XPATH,'//*[@id="comment-0"]/div[1]/div[2]/div[3]/div[1]/span[2]').text
    time.sleep(3)
    info_3 = web.find_element(By.XPATH,'//*[@id="comment-0"]/div[1]/div[2]/div[3]/div[1]/span[51]').text
    good_info = []
    good_info.append(info_1)
    good_info.append(info_2)
    good_info.append(info_3)
    good_info1 = good_info[:2]
    evaluate_date = good_info[-1]
    sel=Selector(text=web.page_source)
    evaluate_time=datetime.strptime(evaluate_date, '%Y-%m-%d %H:%M')
    content_temp=sel.xpath('//*[@id="comment-0"]/div')
    content_list=[]
    for ct in content_temp:
        content="".join(ct.xpath('./div[2]/p/text()').extract()).strip()
        content_list.append(content)
    star="".join(sel.xpath('//*[@id="comment-0"]/div[1]/div[2]/div[1]/@class').extract())
    star=(str(deil(star))+'星')
    comment_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[1]/a/em').text
    comment_nums=deil(comment_nums)
    praised_nums=web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[5]/a/em').text
    praised_nums=deil(praised_nums)
    web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[2]/a').click()
    time.sleep(3)
    image_list_temp =sel.xpath('//*[@id="comment-1"]/div/div/div[1]/div/ul/li')
    time.sleep(2)
    image_list=[]
    for li in image_list_temp:
        src=''.join(li.xpath('./a/img/@src').extract()).strip()
        image_list.append(src)
    web.find_element(By.XPATH,'//*[@id="comment"]/div[2]/div[2]/div[1]/ul/li[3]/a').click()
    time.sleep(3)
    video_list_temp =sel.xpath('//*[@id="comment-2"]/div')
    time.sleep(2)
    video_list=[]
    for vd in video_list_temp:
        video=''.join(vd.xpath('./div[2]/div[3]/div[1]/video/@src').extract()).strip()
        video_list.append(video)
    evaluate=GoodEvaluate()
    evaluate.id=id
    evaluate.good_id=good_id
    evaluate.user_name=user_name
    evaluate.good_info=good_info1
    evaluate.evaluate_time=evaluate_time
    evaluate.content=content_list
    evaluate.star=star
    evaluate.comment_nums=comment_nums
    evaluate.praised_nums=praised_nums
    evaluate.image_list=image_list
    evaluate.save(force_insert=True)
def ges(url):
    web=Chrome()
    web.get(url)
    time.sleep(3)
    sel=Selector(text=web.page_source)
    good_id = re.search('\d+', url).group(0)
    id=good_id
    web.find_element(By.XPATH,'//*[@id="detail"]/div[1]/ul/li[5]').click()
    time.sleep(3)
    tag=sel.xpath('//*[@id="comment"]/div[2]/div[1]/div[2]/div/span')
    tag_list=[]
    for t in tag:
        temp=''.join(t.xpath('./text()').extract())
        tag_list.append(temp)
    num=len(tag_list)
    time.sleep(5)
    ges=GoodEvaluateSummary()
    ges.good_id=good_id
    ges.id=id
    ges.tag=tag_list
    ges.num=num
    ges.save(force_insert=True)
if __name__ == '__main__':
    url="https://item.jd.com/100014348492.html"
    jd_good(url)
    jd_evaluate(url)
    ges(url)