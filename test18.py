# coding:utf-8
# author:YJ沛

def test():
    import json
    info = [{'a':'1','b':'2','c':'3','d':'4','f':'5'}]
    data = json.dumps(info, sort_keys=True, indent=4)
    print(data)


# test()


import datetime
import time

# 计算指定时间的前N天的时间戳
def get_days_time(date, n):
    the_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")
    pre_date = the_date - datetime.timedelta(days=n)
    pre_date = pre_date.strftime('%Y-%m-%d %H:%M:%S')  # 将日期转换为指定的显示格式
    pre_time = time.strptime(pre_date, "%Y-%m-%d %H:%M:%S")  # 将时间转化为数组形式
    print(pre_time)
    pre_stamp = int(time.mktime(pre_time))  # 将时间转化为时间戳形式
    # print(pre_stamp)
    return pre_stamp


date='2021-03-11 00:00:00'
timeStamp = time.strptime(date, "%Y-%m-%d %H:%M:%S")
timeStamp = time.mktime(timeStamp)
print(timeStamp)

date2='2021-03-30 00:00:00'
timeStamp2 = time.strptime(date, "%Y-%m-%d %H:%M:%S")
timeStamp2 = time.mktime(timeStamp2)
print(timeStamp2)



# timeArray = time.localtime()
# print(timeArray)
#
# otherStyleTime = time.strftime('%Y-%m-%d %H:%M:%S', timeArray)
# print("gitlab查询时间：",otherStyleTime)
