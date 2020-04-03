# coding:utf-8
# author:YJ沛

import string
# 生成数字和大小写字母：0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ
print(string.digits+string.ascii_letters)


import winreg

path = u'C:\Program Files (x86)\Tencent\WeChat\WeChat.exe'

#必须以管理员身份运行
class createKey():
    def __init__(self):
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, "FFM")
        key_shell = winreg.CreateKeyEx(key, 'shell', 0, winreg.REG_CREATED_NEW_KEY)
        key_shell_open = winreg.CreateKeyEx(key_shell, 'open', 0, winreg.REG_CREATED_NEW_KEY)

        # 创建数值的名称和值
        winreg.SetValueEx(key, 'URL Protocol', 0, winreg.REG_CREATED_NEW_KEY, u'URL:Go Protocol Handler')  # 设置项中：创建数值的名称和值
        winreg.SetValue(key, 'Defaultlcon', winreg.REG_CREATED_NEW_KEY,
                         path)  # 创建子项并设置键中默认的名称的值
        winreg.SetValue(key_shell_open, 'command', winreg.REG_CREATED_NEW_KEY,
                         path + ' FFM://ffm_ftp')


        winreg.FlushKey(key)
        winreg.CloseKey(key)

        print('set path is ok')

regedit = createKey()




import win32com.client