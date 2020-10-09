# coding:utf-8
# author:YJ沛


import datetime
# 判断 2018年4月30号 是不是节假日
from chinese_calendar import is_workday, is_holiday
april_last = datetime.date(2020, 10, 9)



print("是否为工作日：",is_workday(april_last))
print("是否为节假日：",is_holiday(april_last))

# 或者在判断的同时，获取节日名
import chinese_calendar as calendar  # 也可以这样 import
on_holiday, holiday_name = calendar.get_holiday_detail(april_last)
print(on_holiday)
print(calendar.Holiday.labour_day.value, holiday_name)





# # Python获取一段日期内的工作日和所有日期
import pandas as pd

# 1、获取工作日：bdate_range
e = pd.bdate_range('9/20/2020', '12/31/2020')
# print(e.date) #获取工作日日期列表

# 2、获取所有日期：date_range
e = pd.date_range('9/20/2020', '12/31/2020')
# print(e.date) # 获取所有日期
