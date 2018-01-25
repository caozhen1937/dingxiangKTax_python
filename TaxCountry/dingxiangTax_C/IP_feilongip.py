import random
import re

from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue

from gethtmlTostring import filter_tags
feilongip="http://www.feilongip.com/"
def getfeilongIP():
    error=True
    p_pool = []
    num=1
    print("-开始从飞龙代理爬虫-")
    while error:
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
        try:
            rx = requests.get(feilongip, timeout=15, headers=headers)
            bobj_2 = BeautifulSoup(rx.content.decode('utf-8'), "lxml")
            sibs = bobj_2.findAll("td",{"class","ip"})
            #开始提取页面的IP地址
            for child in  sibs:
                #去除html标签，并且判断是否是IP地址
                if ('.' in filter_tags(str(child))) and (':' in filter_tags(str(child))):
                    p_pool.append(filter_tags(str(child)))
            print("结束")
            error=False
        except Exception as e:
            num=num+1
            if num==5:
                return
            time.sleep(random.randint(1, 6) * 1)
    print("-开始从飞龙代理结束-")
    return p_pool
