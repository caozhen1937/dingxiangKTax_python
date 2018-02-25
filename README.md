# dingxiangKTax_python

丁香税会数据爬虫源代码

##项目概括

1.对中国各大税务相关的网站进行爬虫，收集数据，方便大家搜索并提供各种各种小插件，方便保存文档

2.已将数据对接到http://quanlanguage.com/ （属于本人自建的网站，用于对接爬虫数据），可通过这个网址进行访问（网址是使用nodejs+mysql进行搭建的）

3.如果你对这个项目感兴趣你可以下载app尝试：

  ###1>.小米应用商店：http://app.mi.com/details?id=io.tax.quanlanguage
  
  ###2>.华为应用商店：http://app.hicloud.com/app/C100208479
  
  ###3>.酷安应用商店：https://www.coolapk.com/apk/177007
  
  ###4>.你也可以百度丁香税通进行下载
##项目目前状况

1.项目目前分为三个分支：

1> 国家税务总局（税收法规库）爬虫----分支Taxcountry分支
2> china1266网站爬虫只针对税务总局进行爬虫-----（分支china12366_1.0.0）
3> 国家税务总局最新法规，与法规解读文件 解读爬虫---InterpretationContryTax分支

##国家税务总局最新法规，与法规解读文件 解读爬虫---InterpretationContryTax分支

1.对页面进行拍照，用于判断页面是否更改

2.将数据格式化存储到mysql数据当中

##国家税务总局爬虫（分支Taxcountry分支）概括

1.能对页面进行快照，有助于比较页面是否更改

2.将符合要求数据存入Mysql数据库当中，或进行更新

3.对符合要求的页面按照一定规格进行拍照（俗话：快照），并进行压缩，同时比较前后二次快照，判断页面是否更改

4.模块化自动获取免费代理IP地址，并对获取来的免费IP地址进行校验。

5.利用免费获取的代理ip地址代理去获取免费代理IP，从而达到隐藏自己真实地址（有时）

##国家税务总局爬虫（分支Taxcountry分支）下次版本更新预计新增加功能

1.对失效链接进行标记 （预计推迟）

2.讲网页保存个性化的pdf（预计推迟）

3.可将数据存入mongodb（预计推迟）

##项目运行截图

###1.爬虫页面快照截图

---
![mkdn-scrl-sync](https://github.com/quanlanguage/dingxiangKTax_python/blob/master/TaxCountry/%E5%BF%AB%E7%85%A7%E6%A0%B7%E5%BC%8F.png)
---
###2.运行截图

---
![mkdn-scrl-sync](https://github.com/quanlanguage/dingxiangKTax_python/blob/master/TaxCountry/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE.PNG)
---

##china1266网站爬虫（分支china12366_1.0.0）概括

1.模拟登陆网址（使用自己的账号，目前该网站停止注册）

2.能写入mysql数据库

##china1266网站爬虫（分支china12366_1.0.0）下次版本更新预计新增加功能

1.增加爬虫快照功能

2.增加对mongodb数据库的支持

3.修复已知问题

##运行截图
###1.爬虫搜索截图

---
![mkdn-scrl-sync](https://github.com/quanlanguage/dingxiangKTax_python/blob/master/china12366/%E7%88%AC%E8%99%AB%E6%90%9C%E7%B4%A2%E6%88%AA%E5%9B%BE.png)
---

###2.登陆运行截图

![mkdn-scrl-sync](https://github.com/quanlanguage/dingxiangKTax_python/blob/master/china12366/%E7%99%BB%E9%99%86%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE.png)
---

###3.运行截图

![mkdn-scrl-sync](https://github.com/quanlanguage/dingxiangKTax_python/blob/master/china12366/%E8%BF%90%E8%A1%8C%E6%88%AA%E5%9B%BE.png)
---

##关于作者
如果你有任何问题可通过email联系我：quanlanguage@gmail.com,你也可以在issues这里给我提出问题，我会在第一时间内给你解决

##作者忠告：请勿恶意爬虫



