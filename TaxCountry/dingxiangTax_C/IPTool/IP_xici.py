import random
import re

from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue



#西次ip地址获取 ，页面大小，代理二个参数
from selenium.webdriver.support.wait import WebDriverWait


def getXiCiIP(PageSize,IPaddress):

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
    #设置爬虫页面超时
    driver.set_page_load_timeout(5)
    #从西次进行爬虫
    p_pool = []
    xici_page = 1
    while xici_page <= PageSize:

        new_count = 0
        xici_url = 'http://www.xicidaili.com//wt/' + str(xici_page)
        try:
            max_wait = 5  # 20s
            driver.set_page_load_timeout(max_wait)
            driver.set_script_timeout(max_wait)
            driver.get(xici_url)
            bobj_2 = BeautifulSoup(driver.page_source, "lxml")
            sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
        except Exception as e:
            try:
                print('error 1:', e)
                max_wait = 5  # 20s
                driver.set_page_load_timeout(max_wait)
                driver.set_script_timeout(max_wait)
                driver.get(xici_url)
                # 等待时长6秒，默认0.5秒询问一次
                WebDriverWait(driver, 6)
                bobj_2 = BeautifulSoup(driver.page_source, "lxml")
                sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
            except Exception as e:
                print('error 2', e)
                break
        for sib in sibs:
            try:
                #拼接ip地址
                get_proxy = sib.findAll('td')[1].get_text() + ':' + sib.findAll('td')[2].get_text()
                p_pool.append(get_proxy)
                new_count += 1
            except Exception as e:
                print('error 2', e)
                break
        xici_page += 1
        # 第几个分页面
    return p_pool
