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

from gethtmlTostring import filter_tags
feilongip="http://www.feilongip.com/"
#http://www.goubanjia.com/free/gngn/index.shtml
#获取http代理的ip地址
goubanjia=['http://www.goubanjia.com/free/gngn/','http://www.goubanjia.com/free/gnpt/']

#替黄指定文本 将 none----> 替成 block
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


def goubanjiaIP(Pagesize):
    error=True
    p_pool = []
    num=1
    print("开始-全网代理IP")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}


    for urlItem in goubanjia:
        Haserror=1
        opt = 1
        while opt <=Pagesize:
            #地址
            url=urlItem+"index"+str(opt)+".shtml"
            try:

                chromedriver = r"C:\Users\wangquan\chromedriver\chromedriver.exe"
                os.environ["webdriver.chrome.driver"] = chromedriver
                driver1 = webdriver.Chrome(chromedriver)

                # dcap1 = dict(DesiredCapabilities.PHANTOMJS)
                # dcap1[
                #     "phantomjs.page.settings.userAgent"] = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/53 (KHTML, like Gecko) Chrome/15.0.87"
                #
                # driver1 = webdriver.PhantomJS(executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe', desired_capabilities=dcap1)
                max_wait = 20

                driver1.set_window_size(0, 0)
                driver1.set_page_load_timeout(max_wait)
                driver1.set_script_timeout(max_wait)

                #还原系统代理
                proxy = webdriver.Proxy()
                proxy.proxy_type = ProxyType.DIRECT
                proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                driver1.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

                driver1.get(url)
                time.sleep(2.5)

                #dcap = dict(DesiredCapabilities.PHANTOMJS)  # 设置userAgent
                # dcap["phantomjs.page.settings.userAgent"] = (
                #     "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36")
                # driver = webdriver.PhantomJS(executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe',
                #                              desired_capabilities=dcap,service_args=['--ssl-protocol=any'])
                #
                # # 还原系统代理
                # proxy = webdriver.Proxy()
                # proxy.proxy_type = ProxyType.DIRECT
                # proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
                # driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
                #
                #
                # driver.set_page_load_timeout(20)
                # driver.set_script_timeout(20)  # 这两种设置都进行才有效

                #print(driver.page_source)

                #port=driver.find_element_by_xpath("/html/body/div[4]/div[1]/div[2]/div[5]/div[2]/table/tbody/tr[1]/td[1]/span[9]").text
                #rx = requests.get(url, timeout=15, headers=headers)
                pageSearch=driver1.page_source
                driver1.close()
                driver1.quit()
                bobj_2 = BeautifulSoup(pageSearch, "lxml")
                #获取标签数据
                #print(bobj_2)

                sibs = bobj_2.findAll("td", {"class", "ip"})
            except Exception as e:
                Haserror=Haserror+1
                time.sleep(random.randint(1, 6) * 1)
                if Haserror==3:
                    opt=1000000
            # 开始提取页面的IP地址
            try:
                for child in sibs:
                    # 去除html标签，并且判断是否是IP地址
                    if ('.' in filter_tags(replicFinsh(str(child),'none'))) and (':' in filter_tags(replicFinsh(str(child),'none'))):
                        #添加ip地址到池中
                        p_pool.append(filter_tags(replicFinsh(str(child), 'none')))
                        print(filter_tags(replicFinsh(str(child), 'none')))
                    # print(str(child).replace("\n", ""))
                    #print(str(child))
                opt=opt+1
            except Exception as e:
                Haserror = Haserror + 1
                time.sleep(random.randint(1, 6) * 1)
                if Haserror == 3:
                    opt = 6

    #print(bobj_2)
    print(p_pool)
    print("执行完")
    return p_pool

