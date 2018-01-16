# coding=utf-8
import os
from selenium.webdriver.common.proxy import ProxyType

import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue

_BE_PROXY_QUEUE =queue.Queue()
path="mt_proxy.txt"
path1="mt_proxynew.txt"
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
        requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
        print('ip地址可用')
        return True
    except Exception as e:
        print("IP不可用")
        return False


def get_proxies_from_KDL(max_page):
    #爬虫免费代理ip地址
    base_url = 'http://www.kuaidaili.com/free/'
    options = ['intr/', 'inha/']

    p_pool = []
    xici_page = 1
    while xici_page <= 3:

        new_count = 0

        xici_url = 'http://www.xicidaili.com/nt/' + str(xici_page)
        headers = {
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.86 Safari/537.36'}
        try:
            rx = requests.get(xici_url, timeout=15, headers=headers)
            bobj_2 = BeautifulSoup(rx.content.decode('utf-8'), "lxml")
            sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings
        except Exception as e:
            try:
                #print ('error 1:', e)
                rx = requests.get(xici_url, timeout=15, headers=headers)
                bobj_2 = BeautifulSoup(rx.content.decode('utf-8'), "lxml")
                sibs = bobj_2.findAll('table', {'id': 'ip_list'})[0].tr.next_siblings

            except Exception as e:
                #print ('error 2', e)
                break

        for sib in sibs:
            try:
                get_proxy = sib.findAll('td')[2].get_text() + ':' + sib.findAll('td')[3].get_text()
                p_pool.append(get_proxy)
                new_count += 1
            except AttributeError:
                pass
        xici_page += 1
    # 第几个分页面
    opt = 0


    while opt <= 1:
        page = 1
        while page < max_page:
            url = base_url + options[opt] + str(page) + '/'
            driver = webdriver.PhantomJS(
                executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe')

            #还原系统代理
            proxy = webdriver.Proxy()
            proxy.proxy_type = ProxyType.DIRECT
            proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
            # 隐式等待1秒，可以自己调节
            driver.implicitly_wait(1)
            #开始获取网页
            driver.get(url)
            print(url)
            time.sleep(0.7)
            bobj = BeautifulSoup(driver.page_source,"lxml")
            driver.close()
            siblings = bobj.findAll(name='table', attrs={'class': 'table table-bordered table-striped'})[
                0].tbody.tr.next_siblings
            count = 0
            for sibling in siblings:
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


def geIPmain(path,pageSize):
    # 清空已有的文件
    print("----清空"+path+"-----")
    with open(path, 'w') as f:
        print("清空文件")
    global _BE_PROXY_QUEUE
    max_thread = 100
    threads = []
    # 2大页面，每个大页面3个分页
    pool = get_proxies_from_KDL(pageSize)
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
def getIPList(path1,path2,pageSize):
    #文件不存在创建空文件
    if not file_exists(path1):
        print("判断-文件")
    #若文件不存在创建空文件
    if not file_exists(path2):
        print("判断-文件")
    #ip地址数组
    print(path1+"---"+path2)
    global path
    path=path1
    path2=path2
    ipList = []
    print("开始获取ip地址列表")
    geIPmain(path,pageSize)
    print("获取ip地址结束")
    #去除文本当中的相同ip地址
    Toheavy(path1,path2)
    #读取文件当中的ip地址
    for line in open(path1):
        line = line.strip('\n')
        ipList.append(line)
    return ipList
