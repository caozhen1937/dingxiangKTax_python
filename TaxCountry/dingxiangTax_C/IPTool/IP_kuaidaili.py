import random
import re

from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue


def getKuaidailiIP(max_page,IPaddress):

    driver = webdriver.PhantomJS(
        executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe')
    # 设置系统代理
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.MANUAL
    # 代理ip地址
    proxy.http_proxy = IPaddress
    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    driver.set_page_load_timeout(5)
    #爬虫免费代理ip地址
    base_url = "https://www.kuaidaili.com/free/"
    options = ['intr/', 'inha/']
    p_pool = []
    opt = 0
    while opt <= 1:
        #初始化错误
        error = 1
        page = 1
        while page < max_page:
            #拼接目标URL
            url = base_url + options[opt] +  str(page) + '/'
            print(url)
            # 网页爬虫开始
            try:
                driver.get(url)
                #print(driver.page_source)
                # 隐式等待2秒，可以自己调节
                driver.implicitly_wait(1)
            except:
                # 暂停
                time.sleep(random.randint(1, 6) * 1)
                print("访问页面：已发生第" + str(error - 1) + "次错误")
                error = error + 1
                #退出循环
                if error==6:
                    break
                #终止此次循环
                continue
            #打印此次访问URL地址
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
                    break
                continue
            count = 0
            for sibling in siblings:
                #print(sibling)
                try:
                    get_proxy = sibling.findAll(name='td')[0].get_text() + ':' + sibling.findAll(name='td')[
                        1].get_text()
                    #print(get_proxy)
                    p_pool.append(get_proxy)
                    count += 1
                except AttributeError:
                    pass
            page += 1
        opt += 1
    return p_pool
