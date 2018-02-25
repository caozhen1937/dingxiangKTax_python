#-*- coding:utf-8 -*-
import datetime
import os

import multiprocessing
import re
import threading

import requests
from selenium import webdriver
import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from PIL import ImageFile
from PIL import Image
from PIL import ImageEnhance
from PIL import ImageFilter
import pymysql
import os.path
import random
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from multiprocessing import Process, Lock

from IPTool.IPbuydaxiangdaili import getdaxiangdailiIP
from IPTool_Main.thread_proxy import getIPList

time1 = time.time()

changeIP=False;

#####
# chromedriver = r"C:\Users\wangquan\chromedriver\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
# driver = webdriver.Chrome(chromedriver)
# driver.set_window_size(1200, 900)
# chromedriver = r"C:\Users\wangquan\chromedriver\chromedriver.exe"
# os.environ["webdriver.chrome.driver"] = chromedriver
dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
dcap["phantomjs.page.settings.userAgent"] = (
     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
driver = webdriver.PhantomJS(executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe',
                              desired_capabilities=dcap)
driver.set_window_size(800, 100)
url=""

#存储图片
def saveInterpretationWebSitePageURL(driver,url):
    #print("开始----"+str(id))
    driver.set_window_size(800, 100)
    #设置页面加载超时
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)  # 这两种设置都进行才有效
    # 爬虫开始
    try:
        driver.get(url)
    except TimeoutException:
        print('time out after 10 seconds when loading page')
        driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作

    #获取页面的指定内容
    pagecontent = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[1]/div[2]/span/dl').get_attribute('innerHTML') # 有效程度
    #获取首页文章的url
    getUrl(pagecontent)
    #总页数
    PageNumaber=int((driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[1]/div[2]/table/tbody').text).split(':')[1])

    while True:
        PageNumaber=PageNumaber-1
        print("获取第"+str(PageNumaber)+"页的数据")
        if PageNumaber==0:
            break
        nextpagejs="pageName="+str(PageNumaber)+";goPub('../../n810341/n810760/index_831221_"+str(PageNumaber)+".html')"
        driver.execute_script(nextpagejs)
        time.sleep(5)
        # 获取页面的指定内容
        pagecontent = driver.find_element_by_xpath('/html/body/div[6]/div[1]/div[1]/div[2]/span/dl').get_attribute(
            'innerHTML')  # 有效程度
        # 获取首页文章的url  存入txt文档当中
        getUrl(pagecontent)
#获取url地址
def getUrl(content):
    path="Interpretationurl.txt"
    pattern = '<a.*?href="(.+)".*?>(.*?)</a>'
    print(u'\n获取链接中URL:')
    res_url = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    link = re.findall(res_url, content, re.I | re.S | re.M)
    for url in link:
        with open(path, 'a') as f:
            f.write(url + '\n')

def openfilegetURL(path):
    urlList = []
    #读取文件当中的ip地址
    for line in open(path):
        line = line.strip('\n')
        #若是空行重新开始循环
        if len(line)==0:
            continue
        urlList.append(line)
    return urlList

#访问具体政策解读url地址
def saveInterpretationWebSitePageContent(driver,path):
    urlList=openfilegetURL(path)
    print("开始获取"+str(urlList[0]).replace('../..','http://www.chinatax.gov.cn'))

    driver.set_window_size(800, 100)
    #设置页面加载超时
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)  # 这两种设置都进行才有效
    for urlItem in urlList:
    # 爬虫开始
        try:
            driver.get(str(urlItem).replace('../..','http://www.chinatax.gov.cn'))
        except TimeoutException:
            print('time out after 10 seconds when loading page')
            driver.execute_script('window.stop()')  # 当页面加载时间超过设定时间，通过执行Javascript来stop加载，即可执行后续动作
        #开始对文件进行拍照

        print("开始拍照"+driver.current_url)
        #老快照
        fileBlock='Interpretationimage\\'+str(urlItem).replace('../..','').split("/")[3].replace('c',"")+'_block.png'
        id=str(urlItem).replace('../..','').split("/")[3].replace('c',"")
        #新快照
        fileImage='Interpretationimage\\'+str(urlItem).replace('../..','').split("/")[3].replace('c',"")+'.png'

        # 判断老快照是否存在
        if (os.path.exists(fileBlock)):
            # 生成最新快照
            driver.save_screenshot(fileImage)
            # 压缩图片
            img_zip(fileImage)
            # 判断新旧快照是否一致
            if (equal(fileBlock, fileImage)):
                # 一致删除新快照
                os.remove(fileImage)
            else:
                # 替换旧快照
                os.remove(fileBlock)
                os.rename(fileImage, fileBlock)
                print("替换数据库内容")

                # 标题
                Interpretationtitle = driver.title
                print("标题" + Interpretationtitle)
                # 内容
                Interpretationcontent = driver.find_element_by_xpath("//*[@id='tax_content']").get_attribute('innerHTML')
                # print("内容" + Interpretationcontent)
                # 时间
                Interpretationtime = \
                ((driver.find_element_by_xpath("//div[@class='zuo1']").text).replace(" ", "").replace("来源：", ":")).split(
                    ':')[0] \
                    .replace("年", "-").replace("月", "-").replace("日", "")
                # print("时间"+Interpretationtime)
                # 官网位置
                Interpretationurl = str(urlItem).replace('../..', 'http://www.chinatax.gov.cn')
                # print("官网位置"+Interpretationurl)
                # 发文单位
                try:
                    Interpretationprovenance = (
                    (driver.find_element_by_xpath("//div[@class='zuo1']").text).replace(" ", "").replace("来源：", ":")).split(
                        ':')[1]
                    print("发文单位" + Interpretationprovenance)
                except:
                    Interpretationprovenance = ""

                updateMysql(id,Interpretationtitle, Interpretationtime, Interpretationcontent, Interpretationurl,
                        Interpretationprovenance)

        else:
            driver.save_screenshot(fileBlock)
            # 压缩图片
            img_zip(fileBlock)
            #标题
            Interpretationtitle=driver.title
            print("标题"+Interpretationtitle)
            # 内容
            Interpretationcontent = driver.find_element_by_xpath("//*[@id='tax_content']").get_attribute('innerHTML')
            #print("内容" + Interpretationcontent)
            #/html/body/div[6]/ul[1]/li[3]/div[1]
            # 时间
            Interpretationtime=((driver.find_element_by_xpath("//div[@class='zuo1']").text).replace(" ","").replace("来源：",":")).split(':')[0]\
                .replace("年","-").replace("月","-").replace("日","")
            #print("时间"+Interpretationtime)
            #官网位置
            Interpretationurl=str(urlItem).replace('../..','http://www.chinatax.gov.cn')
            #print("官网位置"+Interpretationurl)
            #发文单位
            try:
                Interpretationprovenance=((driver.find_element_by_xpath("//div[@class='zuo1']").text).replace(" ","").replace("来源：",":")).split(':')[1]
                print("发文单位"+Interpretationprovenance)
            except:
                Interpretationprovenance=""
            #print(driver.page_source)
            saveToMysql(id,Interpretationtitle, Interpretationtime, Interpretationcontent, Interpretationurl,
                        Interpretationprovenance)
        time.sleep(2)

#写入数据库
def saveToMysql(id,Interpretationtitle,Interpretationtime,Interpretationcontent,Interpretationurl,Interpretationprovenance):
    #标题
    #"标题"+Interpretationtitle)
    #"时间"+Interpretationtime)
    #"内容"+Interpretationcontent)
    #"官网位置"+Interpretationurl)
    # "发文单位"+Interpretationprovenance)
    #print(driver.page_source)

    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root",password="root", db="dingxiangktax", port=3306,charset="utf8")
    #INSERT INTO `taxcountry` (`id`, `Country_Title`, `Country_Location`, `Country_Data`, `Country_Info`, `Country_Type`, `Country_url`) VALUES ('1', '2', '2', '2017-12-28', '2', '2', '2')
    cur = conn.cursor()
    Interpretationtitle = str(Interpretationtitle).encode('utf-8').decode()
    Interpretationtime = str(Interpretationtime).encode('utf-8').decode().replace(" ","")
    print(Interpretationtime+"-")
    Interpretationcontent = str(Interpretationcontent).encode('utf-8').decode().replace("'","^")
    Interpretationurl = str(Interpretationurl).encode('utf-8').decode()
    Interpretationprovenance = str(Interpretationprovenance).encode('utf-8').decode()

    sql = u"INSERT INTO `Interpretationcontrytax` (`id`,`Interpretationtitle`, `Interpretationtime`, `Interpretationcontent`, `Interpretationurl`, `Interpretationprovenance`) VALUES ('"+id+"','"+Interpretationtitle+"','"+Interpretationtime+"', '"+Interpretationcontent+"', '"+Interpretationurl+"', '"+Interpretationprovenance+"')"
    sta = cur.execute(sql)
    if sta == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

def updateMysql(id,Interpretationtitle,Interpretationtime,Interpretationcontent,Interpretationurl,Interpretationprovenance):
    print("更新mysql数据")
    #标题
    #"标题"+Interpretationtitle)
    #"时间"+Interpretationtime)
    #"内容"+Interpretationcontent)
    #"官网位置"+Interpretationurl)
    # "发文单位"+Interpretationprovenance)
    #print(driver.page_source)
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root",password="root", db="dingxiangktax", port=3306,charset="utf8")
    #INSERT INTO `taxcountry` (`id`, `Country_Title`, `Country_Location`, `Country_Data`, `Country_Info`, `Country_Type`, `Country_url`) VALUES ('1', '2', '2', '2017-12-28', '2', '2', '2')
    cur = conn.cursor()
    Interpretationtitle = str(Interpretationtitle).encode('utf-8').decode()
    Interpretationtime = str(Interpretationtime).encode('utf-8').decode().replace(" ","")
    Interpretationcontent = str(Interpretationcontent).encode('utf-8').decode().replace("'","^")
    Interpretationurl = str(Interpretationurl).encode('utf-8').decode()
    Interpretationprovenance = str(Interpretationprovenance).encode('utf-8').decode()

    sql=u"UPDATE `Interpretationcontrytax` SET (`Interpretationtitle`='"+Interpretationtitle+"',`Interpretationtime`='"+Interpretationtime\
        +"',`Interpretationcontent`='"+Interpretationcontent+"',`Interpretationurl`='"+Interpretationurl+"',`Interpretationprovenance`='"+Interpretationprovenance+"') WHERE (`id`="+id+")"
    sta = cur.execute(sql)
    conn.commit()
    if sta == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

#判断快照是否一致
def equal(img_file1, img_file2):
    if img_file1 == img_file2:
        return True
    fp1 = open(img_file1, 'rb')
    fp2 = open(img_file2, 'rb')
    img1 = Image.open(fp1)
    img2 = Image.open(fp2)
    ImageFile.LOAD_TRUNCATED_IMAGES = True
    b = img1 == img2
    fp1.close()
    fp2.close()
    return b

#############自定义图像压缩函数############################
def img_zip(path):
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + "：开始压缩完成")
        pngquantPath = r"PNGoo\libs\pngquanti\pngquanti.exe -f --ext .png --quality 50-80 "
        os.system(pngquantPath + path)
        print(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))+"：结束压缩完成")

def cacheDate():
    print("2222")
#时间a减去时间b，获得二者的时间差,参数为时间字符串，例如：2017-03-30 16:54:01.660
def getTimeDiff(timeStra,timeStrb):
    if timeStra<=timeStrb:
        return 0
    ta = time.strptime(timeStra, "%Y-%m-%d %H:%M:%S")
    tb = time.strptime(timeStrb, "%Y-%m-%d %H:%M:%S")
    y,m,d,H,M,S = ta[0:6]
    dataTimea=datetime.datetime(y,m,d,H,M,S)
    y,m,d,H,M,S = tb[0:6]
    dataTimeb=datetime.datetime(y,m,d,H,M,S)
    secondsDiff=(dataTimea-dataTimeb).seconds
        #两者相加得转换成分钟的时间差
    minutesDiff=round(secondsDiff/60,1)
    return minutesDiff

def crawlerMain():

    # 设置代理
    print("开始抓取数据开始："+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #目标url地址
    url = "http://www.chinatax.gov.cn/n810341/n810760/index.html"
    path = "Interpretationurl.txt"
    #获取url  政策解读
    #saveInterpretationWebSitePageURL(driver, url)
    saveInterpretationWebSitePageContent(driver,path)
    print("抓取数据结束：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

##主函数
def startMain():
    #crawlerMain(start, over, IPaddress)
    crawlerMain()
    driver.close()
    driver.quit()
    print("执行完成")

startMain()