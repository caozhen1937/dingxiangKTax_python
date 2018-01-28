# coding=utf-8

import random
import requests
import time
from bs4 import BeautifulSoup
from HTML_Decoding.gethtmlTostring import filter_tags


#飞龙代理已经失效不可用--此代码仅供后来者学习之用
#ip地址大量不可用
def getfeilongIP():
    feilongip = "http://www.feilongip.com/"
    error=True
    p_pool = []
    num=1
    print("-开始从<飞龙代理IP>---获取免费代理ip地址：")
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



