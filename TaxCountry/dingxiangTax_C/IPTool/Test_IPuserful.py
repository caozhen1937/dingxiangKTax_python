# coding=utf-8
import requests

#测试IP地址----http
def test_usefulofHttp(proxy):
    try:
        proxies = {'http': proxy}
        #分析ip地址是否可用，-为我们需要爬虫网页，有效判断是否可用
        requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
        print('ip地址可用：'+proxy)
        return True
    except Exception as e:
        return False

#测试IP地址---https
def test_usefulofHttps(proxy):
    try:
        proxies = {'https': proxy}
        #分析ip地址是否可用，-为我们需要爬虫网页，有效判断是否可用
        requests.get('http://ip.cip.cc', timeout=20, proxies=proxies)
        print('ip地址可用：'+proxy)
        return True
    except Exception as e:
        #print(e)
        return False
