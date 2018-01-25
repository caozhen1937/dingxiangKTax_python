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
def getXiCiIP(PageSize,proxy):
    p_pool = []
    p_pool.append(proxy)
    proxies = {'http': proxy}
    xici_page = 1
    while xici_page <= PageSize:
        #   xicidaili
        new_count = 0
        print('PAGE', str(xici_page))
        xici_url = 'http://www.xicidaili.com//wt/' + str(xici_page)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
        try:
            rx = requests.get(xici_url, timeout=15, headers=headers, proxies=proxies)
            bobj_2 = BeautifulSoup(rx.content.decode('utf-8'), "lxml")
            sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
        except Exception as e:
            try:
                print('error 1:', e)
                rx = requests.get(xici_url, timeout=15, headers=headers, proxies=proxies)
                bobj_2 = BeautifulSoup(rx.content.decode('utf-8'), "lxml")
                sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
            except Exception as e:
                print('error 2', e)
                break

        for sib in sibs:
            try:
                # /html/body/div[1]/div[2]/table/tbody/tr[2]/td[2]
                # sib.find_element_by_xpath("/html/body/div[1]/div[2]/table/tbody/tr[2]/td[2]")
                get_proxy = sib.findAll('td')[1].get_text() + ':' + sib.findAll('td')[2].get_text()
                # print("从西次获取ip地址为："+get_proxy)
                p_pool.append(get_proxy)
                new_count += 1
            except AttributeError:
                pass
        print('get ', new_count, ' proxies in page', xici_page)
        xici_page += 1
        # 第几个分页面
    return p_pool