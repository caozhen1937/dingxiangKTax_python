#-*- coding:utf-8 -*-
import datetime
import os

import multiprocessing
import re
import threading

import requests
from selenium import webdriver
import time
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
chromedriver = r"C:\Users\wangquan\chromedriver\chromedriver.exe"
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.set_window_size(1200, 900)
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
def saveWebSitePage(driver,url,id):
    #print("开始----"+str(id))
    driver.set_window_size(800, 100)
    #设置页面加载超时
    driver.set_page_load_timeout(15)
    driver.set_script_timeout(15)  # 这两种设置都进行才有效
    # 爬虫开始
    try:
        driver.get(url)
    except:
        print("出现未知-错误-----")
        #退出
        time.sleep(0.7)
        return True

    #模仿浏览器的滚动页面行为。
    driver.execute_script("""
        (function () {
          var y = 0;
          var step = 100;
          window.scroll(0, 0);

          function f() {
            if (y < document.body.scrollHeight) {
              y += step;
              window.scroll(0, y);
              setTimeout(f, 50);
            } else {
              window.scroll(0, 0);
              document.title += "scroll-done";
            }
          }
          setTimeout(f, 1000);
        })();
      """)


    #print(driver.page_source)
    if driver.title != "法规详细内容":
        #文章提交失败
        if driver.title=="error":
            #print(driver.find_element_by_xpath('//*[@id="errorInfo"]').text)
            time.sleep(0.8)
            return False
        #服务器未找到相应页面
        if driver.title == "Error 500--Internal Server Error":
            time.sleep(0.8)
            print("500错误")
            return False
        #其他都是服务器拒绝我们要求：402拒绝访问
        time.sleep(0.8)
        return True

    # 正则表达式，判断是否含有数字
    pattern = re.compile('[0-9]+')
    #发布时间含有中文，事务所，过滤不需要
    releaseTime = driver.find_element_by_xpath('//*[@id="cwrq"]').text.split("：")[1]  # 发布时间
    if not pattern.findall(releaseTime):
        time.sleep(1)
        return False
    #有效程度含有数字，事务所过滤不需要的
    effective = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr[5]/td/div/font').text  # 有效程度
    if pattern.findall(effective):
        time.sleep(1)
        return False
    fileTitle = driver.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/div/b/span").text  # 文号标题
    print("文件的标题："+fileTitle)
    #开始对文件进行拍照
    print("开始拍照"+driver.current_url)
    #老快照
    fileBlock='image\\contury'+str(id)+'_block.png'
    #新快照
    fileImage='image\\contury'+str(id)+'.png'

    #判断老快照是否存在
    if(os.path.exists(fileBlock)):
        #生成最新快照
        driver.save_screenshot(fileImage)
        #压缩图片
        img_zip(fileImage)
        #判断新旧快照是否一致
        if (equal(fileBlock, fileImage)):
            #一致删除新快照
            os.remove(fileImage)
        else:
            #替换旧快照
            os.remove(fileBlock)
            os.rename(fileImage,fileBlock)
            print("替换数据库内容")

            fileTitle = driver.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/div/b/span").text  # 文号标题
            fileNumber = driver.find_element_by_xpath('//*[@id="wh"]').text  # 文号编码
            effective = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr[5]/td/div/font').text  # 有效程度
            releaseTime = driver.find_element_by_xpath('//*[@id="cwrq"]').text.split("：")[1]  # 发布时间
            fileContent = driver.find_element_by_xpath('/html/body/div/table[3]/tbody/tr').get_attribute('innerHTML')  # 内容
            updateMysql(str(id), fileTitle, fileNumber, effective, releaseTime, fileContent, url)

    else:
        driver.save_screenshot(fileBlock)
        #压缩图片
        img_zip(fileBlock)
        #c初次写入mysql

        fileTitle = driver.find_element_by_xpath("/html/body/div/table[1]/tbody/tr[2]/td/div/b/span").text  # 文号标题
        fileNumber = driver.find_element_by_xpath('//*[@id="wh"]').text  # 文号编码
        effective = driver.find_element_by_xpath('/html/body/div/table[1]/tbody/tr[5]/td/div/font').text  # 有效程度
        releaseTime = driver.find_element_by_xpath('//*[@id="cwrq"]').text.split("：")[1]  # 发布时间
        fileContent = driver.find_element_by_xpath('/html/body/div/table[3]/tbody/tr').get_attribute('innerHTML')  # 内容
        saveToMysql(str(id),fileTitle,fileNumber,effective,releaseTime,fileContent,url)

    #print(releaseTime)
    return False



#写入数据库
def saveToMysql(id,Country_Title,Country_Location,Country_Type,Country_Data,Country_Info,Country_Url):
    # id 编号
    # Country_Title(标题),
    # Country_Location（位置）,
    # Country_Type（类型）
    # ,Country_Data（日期）,
    # Country_Info（内容）
    #Country_Url  链接
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root",password="root", db="dingxiangktax", port=3306,charset="utf8")
    #INSERT INTO `taxcountry` (`id`, `Country_Title`, `Country_Location`, `Country_Data`, `Country_Info`, `Country_Type`, `Country_url`) VALUES ('1', '2', '2', '2017-12-28', '2', '2', '2')
    cur = conn.cursor()
    Country_Title = str(Country_Title).encode('utf-8').decode()
    Country_Location = str(Country_Location).encode('utf-8').decode()
    Country_Type = str(Country_Type).encode('utf-8').decode()
    Country_Data = str(Country_Data).encode('utf-8').decode()
    Country_Info = str(Country_Info).encode('utf-8').decode().replace("'","^")
    Country_Url=str(Country_Url).encode('utf-8').decode()
    sql = u"INSERT INTO `taxcountry` (`id`, `Country_Title`, `Country_Location`, `Country_Data`, `Country_Info`, `Country_Type`, `Country_Url`)  VALUES ('"+id+"', '"+Country_Title+"', '"+Country_Location+"', '"+Country_Data+"', '"+Country_Info+"', '"+Country_Type+"', '"+Country_Url+"')"
    sta = cur.execute(sql)
    if sta == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()

def updateMysql(id,Country_Title,Country_Location,Country_Type,Country_Data,Country_Info,Country_Url):
    print("更新mysql数据")
    # id 编号
    # Country_Title(标题),
    # Country_Location（位置）,
    # Country_Type（类型）
    # ,Country_Data（日期）,
    # Country_Info（内容）
    #Country_Url  链接
    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root",password="root", db="dingxiangktax", port=3306,charset="utf8")
    cur = conn.cursor()
    Country_Title = str(Country_Title).encode('utf-8').decode()
    Country_Location = str(Country_Location).encode('utf-8').decode()
    Country_Type = str(Country_Type).encode('utf-8').decode()
    Country_Data = str(Country_Data).encode('utf-8').decode()
    Country_Info = str(Country_Info).encode('utf-8').decode().replace("'","^")
    Country_Url=str(Country_Url).encode('utf-8').decode()
    sql=u"UPDATE `taxcountry` SET `Country_Title` = '"+Country_Title+"', `Country_Location` = '"+Country_Location+"', `Country_Data` = '"+Country_Data+"', `Country_Info` = '"+Country_Info+"', `Country_Type` = '"+Country_Type+"', `Country_Url` = '"+Country_Url+"' WHERE(`id` = '"+id+"')"
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

IPList=[]

def crawlerMain(start):

    # 设置代理
    print("第" + str(start) + "次循环开始循环："+ time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
    #开始循环爬虫
    #链接地址
    url = "http://hd.chinatax.gov.cn/guoshui/action/GetArticleView1.do?id=" + str(start) + "&flag=1"
    changeIP = saveWebSitePage(driver, url, start)
    print("第" + str(start) + "次循环开始循环：" + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))

##主函数
def startMain(start):
    #crawlerMain(start, over, IPaddress)
    crawlerMain(start)
    driver.close()
    driver.quit()
    print("执行完成")

startMain(299328)






