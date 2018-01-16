import _main

IPaddress = '115.46.72.116:8123' #默认设置代理地址
print("开始爬虫")
path="1.txt"    #存放未去重ip地址
path1="2.txt"   #存放去重Ip地址
pageSize=3      #免费代理的页数
_main.startMain(101779,110000,IPaddress,path,path1,pageSize)
print("结束")
