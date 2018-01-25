# coding=utf-8
import os
import random

from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue
from IP_goubanjia import goubanjiaIP
from IP_feilongip import getfeilongIP
from IP_kuaidaili import getKuaidailiIP
from IP_xici import getXiCiIP

_BE_PROXY_QUEUE =queue.Queue()

class Consumer_Thread(Thread):
    def run(self):
        global _BE_PROXY_QUEUE
        while not _BE_PROXY_QUEUE.empty():
            p = _BE_PROXY_QUEUE.get()
            try:
                if test_useful(p):
                    with open(path, 'a') as f:
                        f.write(p + '\n')
            except Exception as e:
                #print('[HERE]', e)
                pass
            finally:
                _BE_PROXY_QUEUE.task_done()

#测试IP地址是否可用
def test_useful(proxy):
    try:
        proxies = {'http': proxy}
        #分析ip地址是否可用，-为我们需要爬虫网页，有效判断是否可用
        requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
        print('ip地址可用：'+proxy)
        return True
    except Exception as e:
        #print(e)
        return False


def get_proxies_from_KDL(goubanjiaP,max_page):
    #爬虫免费代理ip地址
    p_pool = []

    #获取免费ip地址开始
    p_pool.extend(goubanjiaIP(goubanjiaP))
    p_pool.extend(getfeilongIP())
    p_pool.extend(getKuaidailiIP(max_page))
    
    #判断数组的长度
    if len(p_pool):
        p_pool.extend(getXiCiIP(max_page,p_pool[0]))
    else:
        time.sleep(5)
        p_pool=get_proxies_from_KDL(goubanjiaP,max_page)
    #数组去重
    p_pool = list(set(p_pool))
    return p_pool


def get_proxies_from_file():
    with open('proxy_kdl.txt', 'r') as f:
        return f.readlines()


def test_proxies_efficience(proxy):
    proxies = {'http': proxy}
    start = time.time()
    for i in range(3):
        r = requests.get('http://www.baidu.com', proxies=proxies)
        #print (i, '  ', r.text)
    cost = time.time() - start
    #print ('With Proxy: cost ', cost / 3, ' seconds')
    start = time.time()
    for i in range(3):
        r = requests.get('http://ip.cip.cc')
        #print (i, '  ', r.text)
    cost = time.time() - start
    #print ('Without Proxy: cost ', cost / 3, ' seconds')


def geIPmain(path,goubanjiaP,max_page):
    # 清空已有的文件
    print("----清空"+path+"-----")
    with open(path, 'w') as f:
        print("清空文件")
    global _BE_PROXY_QUEUE
    max_thread = 100
    threads = []
    # 2大页面，每个大页面3个分页
    pool = get_proxies_from_KDL(goubanjiaP,max_page)
    for i in range(len(pool)):
        _BE_PROXY_QUEUE.put(pool[i])
    for i in range(max_thread):
        threads.append(Consumer_Thread())
    for i in range(max_thread):
        threads[i].start()
    # 陷入等待 线程不够 是因为线程没有死循环就退出
    _BE_PROXY_QUEUE.join()
    print ('已成功获取ip地址')

#去除相同ip地址
def Toheavy(path1,path2):
    outfile = open(path2, 'w')  # 新的文件
    list_1 = []
    for line in open(path1):  # 老文件
        tmp = line.strip()
        #空行去除
        if len(tmp)==0:
            continue
        if tmp not in list_1:
            list_1.append(tmp)
            outfile.write(line)
    outfile.close()

#判断文件是否存在
def file_exists(filename):
    try:
        with open(filename,'w') as f:
            return True
    except IOError:
        return False


#爬虫可用ip地址   path1= mt_proxy.txt
#去重一行ip地址   path2 = 'mt_proxynew.txt'
#pageSize:爬虫页面大小
#放回ip地址数组
def getIPList(path1,path2,goubanjiaP,max_page):
    #文件不存在创建空文件
    if not file_exists(path1):
        print("判断-文件")
    #若文件不存在创建空文件
    if not file_exists(path2):
        print("判断-文件")
    #ip地址数组
    global path
    path=path1
    path2=path2
    ipList = []
    print("开始获取ip地址列表")
    geIPmain(path,goubanjiaP,max_page)
    print("获取ip地址结束")
    #去除文本当中的相同ip地址
    Toheavy(path1,path2)
    #读取文件当中的ip地址
    for line in open(path2):
        line = line.strip('\n')
        #若是空行重新开始循环
        if len(line)==0:
            continue
        ipList.append(line)
    return ipList
