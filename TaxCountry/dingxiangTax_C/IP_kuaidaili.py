import random
import re

from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue


def getKuaidailiIP(max_page):
    #爬虫免费代理ip地址
    base_url = 'http://www.kuaidaili.com/free/'
    options = ['intr/', 'inha/']
    p_pool = []
    opt = 0
    #错误个数
    error=1
    while opt <= 1:
        #初始化错误
        error = 1
        page = 1
        while page < max_page:
            #随机取去页数
            url = base_url + options[opt] +  str(page) + '/'
            driver = webdriver.PhantomJS(
                executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe')

            # 设置页面加载超时
            driver.set_page_load_timeout(15)

            #还原系统代理
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.DIRECT
            proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
            # 隐式等待1秒，可以自己调节
            driver.implicitly_wait(1)

            # 网页爬虫开始
            try:
                driver.get(url)
            except:
                print("出现未知-错误-----")
                # 暂停
                time.sleep(random.randint(1, 6) * 1)
                print("访问页面：已发生第" + str(error - 1) + "次错误")
                error = error + 1
                #退出循环
                if error==6:
                    error=1
                    break
                #终止此次循环
                continue
            #打印此次访问URL地址
            print(url)
            time.sleep(0.7)
            bobj = BeautifulSoup(driver.page_source,"lxml")
            driver.close()
            try:
                siblings = bobj.findAll(name='table', attrs={'class': 'table table-bordered table-striped'})[
                    0].tbody.tr.next_siblings
            except Exception as e:
                error=error+1
                #随机等待
                time.sleep(random.randint(1, 6) * 1)
                print("访问页面：已发生第"+str(error-1)+"次错误")
                #如果连续五次错误退出
                if error==6:
                    error=1
                    break
                continue
            count = 0
            for sibling in siblings:
                try:
                    get_proxy = sibling.findAll(name='td')[0].get_text() + ':' + sibling.findAll(name='td')[
                        1].get_text()
                    p_pool.append(get_proxy)
                    count += 1
                except AttributeError:
                    pass
            page += 1
        opt += 1
    return p_pool