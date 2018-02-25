import _main

IPaddress = '115.46.72.116:8123' #默认设置代理地址
print("开始爬虫")
path="1.txt"    #存放未去重ip地址
path1="1OLD.txt"   #存放去重Ip地址
pageSize=4      #免费代理的页数
max_page=4
_main.startMain(6061657,7000000,IPaddress,path,path1,pageSize,max_page)
print("结束")
