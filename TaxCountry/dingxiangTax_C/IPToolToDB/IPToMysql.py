


import pymysql

#写入数据库
def saveIPadressToMysql(address):

    # address ip代理IP地址

    # 打开数据库连接
    conn = pymysql.connect(host="localhost", user="root",password="root", db="dingxiangktax", port=3306,charset="utf8")
    cur = conn.cursor()
    address = str(address).encode('utf-8').decode()
    sql = u""
    sta = cur.execute(sql)
    if sta == 1:
        print('Done')
    else:
        print('Failed')
    conn.commit()
    cur.close()
    conn.close()
