import requests
# import cv2 as cv
from lxml import html
import urllib.request
from urllib.parse import quote
import os
import time
from urllib import request
import string
import ssl

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

save_path = "..//img//"

# 输出时间
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def testWeather():
    r = requests.get('http://www.weather.com.cn/data/sk/101210101.html')
    print(r.content)
    r.encoding = 'utf-8'
    print(r.json())



# 豆瓣读书
def captureDouBan():
    url='https://book.douban.com/' #需要爬数据的网址
    page=requests.Session().get(url)
    tree=html.fromstring(page.text)
    result=tree.xpath('//div[@class="cover"]//a//img') #获取需要的数据
    # pic = result.
    for item in result:
        src = item.xpath('@src')[0]
        alt = item.xpath('@alt')[0]
        print(item.xpath('@src'), item.xpath('@alt'))
        # content = savepath + str(index) +".jpg";
        # print(content)
        request.urlretrieve(src, "E://tangliangdong//python3//img//"+alt+".jpg")

#桌面壁纸
def captureDestop():
    url = 'http://desk.zol.com.cn/meinv/1920x1080/hot_1.html'
    url = 'http://www.obzhi.com/'

    page = requests.Session().get(url)
    tree = html.fromstring(page.text)
    result = tree.xpath('//div[@class="thumbnail"]//a[@class="zoom"]//img')  # 获取需要的数据
    for item in result:
        src = quote(item.xpath('@src')[0], safe=string.printable)
        # src = quote(item.xpath('@src')[0])
        alt = str(item.xpath('@alt')[0])
        if type(src) == str:
            print("字符串")
        print(src, alt)
        request.urlretrieve(src, "E://tangliangdong//python3//img//壁纸//" + alt + ".jpg")


def captureGirlDestop():
    path = save_path + "壁纸//girl//"
    if(not os.path.exists(path)):
        os.makedirs(path)

    index = 1;
    while(index <= 100):
        num = 1;
        url = 'http://desk.zol.com.cn/meinv/1920x1080/hot_'+str(index)+'.html'
        page = requests.Session().get(url)
        page.encoding='gbk'
        tree = html.fromstring(page.text)
        img_path = path + str(index)
        result = tree.xpath('//ul[contains(@class, "pic-list2")]//li[@class="photo-list-padding"]//a//img')  # 获取需要的数据
        if len(result) == 0:
            print("没有新的页面了")
            return
        if not os.path.exists(img_path): #创建文件夹
            os.makedirs(img_path)

        for item in result:
            src = quote(item.xpath('@src')[0], safe=string.printable)
            alt = item.xpath('@alt')[0]
            print(src, alt, num)
            num+=1
            request.urlretrieve(src, img_path + "//" + alt + ".jpg")

        index += 1
        time.sleep(2)


def captureBigPicture(path, url, imgName):
    print(path, url)
    page = requests.Session().get(url)
    tree = html.fromstring(page.text)
    result = tree.xpath('//img[@id="bigImg"]/@src')  # 获取需要的数据
    print('图片地址', result)
    if(len(result) ==0):
        print('没找到大图')
        return
    request.urlretrieve(result[0], path + "//" + imgName + ".jpg")


def capturePicture(path, url, pre_url):
    if(not os.path.exists(path)):
        os.makedirs(path)

    index = 0;
    while(index <= 5):
        if index == 0:
            visit_url = url
        else:
            visit_url = url + str(index) + '.html'

        page = requests.Session().get(visit_url)
        page.encoding='gbk'
        tree = html.fromstring(page.text)
        img_path = path + str(index)
        result = tree.xpath('//ul[contains(@class, "pic-list2")]//li[@class="photo-list-padding"]//a')  # 获取需要的数据
        if len(result) == 0:
            print("没有新的图片了")
            return
        if not os.path.exists(img_path): #创建文件夹
            os.makedirs(img_path)
        print("保存在" + img_path)

        for item in result:
            src = quote(item.xpath('@href')[0], safe=string.printable)
            name = item.xpath('img/@alt')[0]
            # try:
            #     captureBigPicture(img_path, pre_url+src, name)
            # except OSError:
            #     print("Error: 写入文件失败")
            captureBigPicture(img_path, pre_url + src, name)

        index += 1
        time.sleep(2)

def capturePictureHome():
    home_url = "http://desk.zol.com.cn/"
    path = save_path + "壁纸//首页//"
    if(not os.path.exists(path)):
        os.makedirs(path)

    page = requests.Session().get(home_url)
    page.encoding='gbk'
    tree = html.fromstring(page.text)
    result = tree.xpath('//dd[contains(@class, "brand-sel-box")]//a')  # 获取需要的数据
    result = list(set(result))
    for item in result:
        title = item.xpath("text()")[0]

        src = item.xpath('@href')
        if len(src) == 0:
            continue

        print(title, src)

        capturePicture(path+title+"//", home_url + src[0], home_url)

if __name__=="__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    # testWeather()
    capturePictureHome()
    # captureGirlDestop()

    # BlockingScheduler
    # scheduler = BlockingScheduler()
    # # scheduler.add_job(job, 'cron', day_of_week='1-5', hour=6, minute=30)
    # scheduler.add_job(job, 'interval', seconds=5)
    #
    # scheduler.start()
    # scheduler.print_jobs()

    # print('\n'.join([''.join([('IloveU'[(x-y)%len('IloveU')]if((x*0.05)**2+(y*0.1)**2-1)**3-(x*0.05)**2*(y*0.1)**3<=0 else' ')for x in range(-30,30)])for y in range(15,-15,-1)]))