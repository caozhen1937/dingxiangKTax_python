# coding=utf-8

#判断文件是否存在
def file_exists(filename):
    try:
        with open(filename,'r') as f:
            return True
    except IOError:
        return False

#去除文件当中相同行，用于去除相同ip地址，
#传入参数，path1 文件 path2 修改之后文件
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

