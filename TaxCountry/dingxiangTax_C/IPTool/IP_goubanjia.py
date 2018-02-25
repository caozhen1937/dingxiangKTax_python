import random
import re

import os
from selenium.webdriver import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue

from HTML_Decoding.gethtmlTostring import filter_tags


#针对全网代理IP 页面标签混乱的问题提出一种解决方案原因
#1.我们熟知的HTML标签始终是封闭的
#2.所有的行内样式为display：none 均为我们不需要的内容
#具体方案如下
#1.将所有的判断字符串中是否有none，再进行逐个字符串的比较--遇到<标签时结束，并将none改成block
#2.去除标签内的所有的html标签，
#3.最终文本就可展示出来

#替换指定文本 将 none----> 替成 block
def replicNone(Lstr,searchStr):
    opt=Lstr.find(searchStr)
    #判断是否含有不符合要求的标签
    if  Lstr.find(searchStr) == -1:
        return Lstr
    num=0
    find=True
    repliceStr="n"
    #进行替换
    while find:
        num = num + 1
        if Lstr[opt+num]=='<':
            find=False
        repliceStr=repliceStr+Lstr[opt+num]
    #将不符合要求的标签去空，更改属性为block
    Lstr=Lstr.replace(repliceStr, 'block;"><')
    return Lstr

#查找display：none 均为不符合要求的，-替换文本
def replicFinsh(Lstr,searchStr):
    #去掉换行
    Lstr = Lstr.replace("\n", "")
    find=True
    while find:
        Lstr=replicNone(Lstr,searchStr)
        if Lstr.find(searchStr) == -1:
            find=False
    return Lstr


#Pagesize：页面的大小，IPaddress，代理ip地址
def goubanjiaIP(Pagesize,IPaddress):
    # 全网代理ip地址网址数组
    goubanjia = ['http://www.goubanjia.com/free/gngn/', 'http://www.goubanjia.com/free/gnpt/']
    print("开始从《全网代理ip》----中获取免费的代理ip地址")

    #使用chromedriver模拟页面打开
    chromedriver = r"C:\Users\wangquan\chromedriver\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver1 = webdriver.Chrome(chromedriver)
    #用于存储格式化之后的ip地址
    p_pool = []
    #设置窗体大小
    driver1.set_window_size(0, 0)
    #设置窗体的位置
    driver1.set_window_position(-200,-200)
    # 设置系统代理
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    # 代理ip地址
    proxy.http_proxy = IPaddress
    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    driver1.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    for urlItem in goubanjia:
        Haserror=1
        opt = 1
        while opt <=Pagesize:
            #地址
            url=urlItem+"index"+str(opt)+".shtml"
            try:
                # 设置爬虫页面超时
                driver1.set_page_load_timeout(5)
                #访问目标地址
                driver1.get(url)
                time.sleep(0.5)
                #获取页面信息
                pageSearch=driver1.page_source
                #对页面数据进行转码
                bobj_2 = BeautifulSoup(pageSearch, "lxml")
                #获取指定标签数据
                sibs = bobj_2.findAll("td", {"class", "ip"})
                #开始解析页面
                for child in sibs:
                    # 去除html标签，并且判断是否是IP地址
                    if ('.' in filter_tags(replicFinsh(str(child),'none'))) and (':' in filter_tags(replicFinsh(str(child),'none'))):
                        #添加ip地址到池中
                        p_pool.append(filter_tags(replicFinsh(str(child), 'none')))
                        #print(filter_tags(replicFinsh(str(child), 'none')))
                opt=opt+1
            except Exception as e:
                Haserror=Haserror+1
                #页面等待，之后再次访问页面来获取数据
                time.sleep(random.randint(1, 6) * 0.1)
                #此次页面获取失败
                if Haserror==3:
                    opt=1000000

    driver1.close()
    driver1.quit()
    return p_pool
