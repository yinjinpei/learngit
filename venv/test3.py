#-*- coding:utf-8 -*-
#author:YJ沛

from __future__ import unicode_literals
from threading import Timer
from wxpy import  *
import time,datetime

bot = Bot(cache_path=True)
a = bot.friends(update=True)
print(type(a))
print(a)