# -*- coding:utf-8 -*-
import win32com.client as win32
import warnings
import sys

reload(sys)
sys.setdefaultencoding('utf8')
warnings.filterwarnings('ignore')


def sendemail(sub, body):
    outlook = win32.Dispatch('outlook.application')
    receivers = ['xxxx@pingan.com.cn;xxxx@pingan.com.cn;xxxx@pingan.com.cn']
    mail = outlook.CreateItem(0)
    mail.To = receivers[0]
    mail.Subject = sub.decode('utf-8')
    mail.Body = body.decode('utf-8')
    # 添加附件
    # mail.Attachments.Add('D:\Users\xxx\Desktop\email.log')
    mail.Send()

