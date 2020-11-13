# coding:utf-8
# author:YJ沛


import os

def zipDir(sourcePath, outFullName, password=None):
    """
    压缩指定文件夹
    :param sourcePath: 目标文件夹路径
    :param outFullName: 保存路径+xxxx.zip
    :return:
    """

    print('sourcePath: ',sourcePath)
    print('sourcePath: ',outFullName)
    print('password: ',password)

    if password:
        cmd = "zip -P %s -r %s %s" % (password, outFullName, sourcePath)   #有密码时设置密码并压缩
    else:
        cmd = "zip -r %s %s" % (outFullName, sourcePath)   #无密码直接压缩

    # 执行系统命令
    status = os.popen(cmd)
    print(status)

    return outFullName


print(os.listdir('project_one'))

sourcePath='project_one'
outFullName='project_one\\project_one.zip'
password='abc123'

# a=zipDir(sourcePath,outFullName)
# print(a)

import platform

# python判断当前系统是Windows or Linux
if __name__ == '__main__':
    sys = platform.system()
    if sys == "Windows":
        print("OS is Windows!!!")
    elif sys == "Linux":
        print("OS is Linux!!!")
        pass
    else:
        pass



# python自身有一个比较好的包 tarfile以及zipfile都可以压缩文件，但是当我们需要加密压缩文件的时候，这两个包无法提供，
# 根据官方资料 zipfile的setpassword 是无法设置密码的
# ZipFile.setpassword(pwd)：
# 	Set pwd as default password to extract encrypted files
# 可以看到只能用在提取加密的文件的时候（解压）才能有效，详情见这里
# 另辟蹊径
# 利用脚本调用命令并压缩添加文件的方式（支持linux与window），主要方式是压缩用命令方式，解压用zipFile并设置密码解压
import subprocess
import zipfile as zf
import platform as pf
import os

class ZipObj():

    def __init__(self, filepathname, passwd):
        self.filepathname = filepathname
        self.passwd = passwd.encode('utf-8')

    def enCrypt(self, deleteSource=False):
        """
	        压缩加密，并删除原数据
            window系统调用rar程序

            linux等其他系统调用内置命令 zip -P123 tar source
            默认不删除原文件
        """
        target = self.filepathname + ".zip"
        source = self.filepathname + ".txt"
        if pf.system() == "Windows":
            cmd = ['rar', 'a', '-p%s' % (self.passwd.encode('utf-8')), target, source]
            p = subprocess.Popen(cmd, executable=r'C:\Program Files\WinRAR\WinRAR.exe')
            p.wait()
        else:
            cmd = ['zip', '-P %s' % (self.passwd.encode('utf-8')), target, source]
            p = subprocess.Popen(cmd)
            p.wait()
        #            os.system(" ".join(cmd))
        if deleteSource:
            os.remove(source)

    def deCrypt(self):
        """
        使用之前先创造ZipObj类
        解压文件
        """
        zfile = zf.ZipFile(self.filepathname + ".zip")
        zfile.extractall(r"zipdata", pwd=self.passwd.encode('utf-8'))


if __name__ == "__main__":
    zipo = ZipObj("文件名", "文件密码")
    #    zipo.enCrypt(deleteSource=False) ##
    zipo.deCrypt()