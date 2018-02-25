# coding=utf-8

import time
from threading import Thread
import queue

from IPTool.IP_goubanjia import goubanjiaIP
from IPTool.IP_kuaidaili import getKuaidailiIP
from IPTool.IP_xici import getXiCiIP
from IPTool.Test_IPuserful import test_usefulofHttp
from Tool.file import file_exists, Toheavy

_BE_PROXY_QUEUE =queue.Queue()

class Consumer_Thread(Thread):
    def run(self):
        global _BE_PROXY_QUEUE
        while not _BE_PROXY_QUEUE.empty():
            p = _BE_PROXY_QUEUE.get()
            try:
                if p=="127.0.0.1:1080":
                    with open(path, 'a') as f:
                        f.write(p + '\n')
                if test_usefulofHttp(p):
                    with open(path, 'a') as f:
                        f.write(p + '\n')
            except Exception as e:
                pass
            finally:
                _BE_PROXY_QUEUE.task_done()


def getNewAddressIP(IPaddressList,goubanjiaP,max_page):
    #guoban=[]
    Kuaidaili=[]
    xici=[]
    ipList = []
    for address in IPaddressList:
        # if not len(guoban):
        #     guoban.extend(goubanjiaIP(goubanjiaP,address))
        #     ipList.extend(guoban)
        if not len(Kuaidaili):
            Kuaidaili.extend(getKuaidailiIP(max_page,address))
            ipList.extend(Kuaidaili)
        if not len(xici):
            xici.extend(getXiCiIP(max_page,address))
            ipList.extend(xici)
        #若找到代理IP则终止循环
        if (len(Kuaidaili) and len(xici)) or len(xici):
            break
    return ipList

def get_proxies_from_KDL(path2,goubanjiaP,max_page):

    #读取文件中的ip地址
    IPaddress=getIPfromFile(path2)
    p_pool = []
    #若文件中含有ip地址则利用此ip地址进行爬虫
    if len(IPaddress):
        p_pool.extend(getNewAddressIP(IPaddress,goubanjiaP,max_page))
    if not len(p_pool):
        #添加本地代理
        p_pool.append("127.0.0.1:1080")
    #数组对爬虫ip地址去重
    p_pool = list(set(p_pool))
    return p_pool

def geIPmain(path,path2,goubanjiaP,max_page):
    # 清空已有的文件
    print("----清空"+path+"-----")
    with open(path, 'w') as f:
        print("清空文件")
    global _BE_PROXY_QUEUE
    max_thread = 100
    threads = []

    # 2大页面，每个大页面3个分页
    pool = get_proxies_from_KDL(path2,goubanjiaP,max_page)

    for i in range(len(pool)):
        _BE_PROXY_QUEUE.put(pool[i])
    for i in range(max_thread):
        threads.append(Consumer_Thread())
    for i in range(max_thread):
        threads[i].start()
    # 陷入等待 线程不够 是因为线程没有死循环就退出
    _BE_PROXY_QUEUE.join()
    print ('已成功获取ip地址')


def getIPfromFile(path):
    ipList = []
    #读取文件当中的ip地址
    for line in open(path):
        line = line.strip('\n')
        #若是空行重新开始循环
        if len(line)==0:
            continue
        ipList.append(line)
    return ipList


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

    print("开始获取ip地址列表")
    geIPmain(path,path2,goubanjiaP,max_page)
    print("获取ip地址结束")
    #去除文本当中的相同ip地址
    Toheavy(path1,path2)
    return getIPfromFile(path2)

