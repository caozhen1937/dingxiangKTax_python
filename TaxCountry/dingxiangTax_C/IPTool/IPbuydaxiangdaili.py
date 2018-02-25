import random
import re
from selenium.webdriver.common.proxy import ProxyType
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from threading import Thread
import queue

from HTML_Decoding.gethtmlTostring import filter_tags
#西次ip地址获取 ，页面大小，代理二个参数
from selenium.webdriver.support.wait import WebDriverWait

#匹配是否有ip地址
def ip_exist(text):
    compile_rule = re.compile(r'(?<![\.\d])(?:\d{1,3}\.){3}\d{1,3}(?![\.\d])')
    match_list = re.findall(compile_rule, text)
    if match_list:
        return True
    else:
        return False

def getdaxiangdailiIP():
    driver = webdriver.PhantomJS(
        executable_path=r'C:\Users\wangquan\phantomjs\bin\phantomjs.exe')
    # 设置页面加载超时
    daxiangurl="http://tvp.daxiangdaili.com/ip/?tid=556249540865397&num=1&protocol=http"
    driver.set_page_load_timeout(5)
    # 还原系统代理
    proxy = webdriver.Proxy()
    proxy.proxy_type = ProxyType.DIRECT
    # 代理ip地址
    # 将代理设置添加到webdriver.DesiredCapabilities.PHANTOMJS中
    proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
    driver.start_session(webdriver.DesiredCapabilities.PHANTOMJS)
    time.sleep(1.5)
    Retuenip=""
    while True:
        driver.get(daxiangurl)
        Retuenip=filter_tags(driver.page_source)
        if ip_exist(Retuenip):
            print("正确获取ip地址-开始爬虫："+Retuenip)
            break
        else:
            print("获取ip地址失败正在重新获取")
        time.sleep(1.5)
    #返回IP地址
    return Retuenip