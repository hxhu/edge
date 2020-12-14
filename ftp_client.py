 # -*- coding: utf-8 -*-
 # python 27
 # 2018.12.27
 # 实现从ftp上下载文件到本地
from ftplib import FTP
import datetime
import os

def ftpconnect(host, username, password):
    ftp = FTP()  # 设置变量
    timeout = 30
    port = 21
    ftp.connect(host, port, timeout)  # 连接FTP服务器
    print("connect success")
    ftp.login(username, password)  # 登录
    print("login success")
    return ftp

def downloadfile(ftp, remotepath, localpath, filename):
    result = False

    ftp.cwd(remotepath)  # 设置FTP远程目录(路径)
    list = ftp.nlst()  # 获取目录下的文件,获得目录列表
    for name in list:
        if name == filename:
            path = localpath + name  # 定义文件保存路径
            f = open(path, 'wb')  # 打开要保存文件
            filename = 'RETR ' + name  # 保存FTP文件
            ftp.retrbinary(filename, f.write)  # 保存FTP上的文件
            print("download " + name + " success")
            result = True
    ftp.set_debuglevel(0)  # 关闭调试
    f.close()  # 关闭文件
    return result

# message:{"command":"pushModelpoints","data":"/home/ftpdir/models/yolov3.weights;N1334859111304531968","target":"N1334896073990213632;1234567890","timestamp":1607306166855}
def pushModel(data):
    print("========== download model ===========")
    print(datetime.datetime.now())
    source = data.split(";")
    sourceList = source[0].split("/")
    
    remotepath = "/"
    for i in range(1,len(sourceList)-1):
        remotepath += sourceList[i] + "/"
    localpath = "./model/"
    filename = sourceList[(len(sourceList)-1)]
    
    result = False
    ftp = ftpconnect('47.94.44.231', "ftpdir", '123456')
    result = downloadfile(ftp, remotepath, localpath, filename)
    ftp.quit()
    print("=====================================")

    return result

if __name__ == "__main__":
    data = "/home/ftpdir/models/yolov3.weights;N1334859111304531968"
    pushModel(data)