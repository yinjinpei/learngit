# coding:utf-8

import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

def job():
    print('执行一次任务')


MyJobID=datetime.now().strftime("%Y%m%d%H%M%S")
sched = BackgroundScheduler()
sched.add_job(job, 'interval',id=MyJobID, minutes=1,next_run_time=datetime.now(), start_date='2020-10-26 22:12:11', end_date='2020-10-26 23:00:00')
sched.start()

while True:
    time.sleep(1)
    print(sched.get_jobs())
    # print(sched.print_jobs())

#
# # 引入模块
# import time, datetime
#
# # str类型的日期转换为时间戳
#
# # 字符类型的时间
# tss1 = '2013-10-10 23:40:00'
# # 转为时间数组
# timeArray = time.strptime(tss1, "%Y-%m-%d %H:%M:%S")
# # print timeArray
# # timeArray可以调用tm_year等
# # print timeArray.tm_year   # 2013
# # 转为时间戳
# timeStamp = int(time.mktime(timeArray))
# # print timeStamp  # 1381419600
#
#
# # 更改str类型日期的显示格式
# tss2 = "2013-10-10 23:40:00"
# # 转为数组
# timeArray = time.strptime(tss2, "%Y-%m-%d %H:%M:%S")
# # 转为其它显示格式
# otherStyleTime = time.strftime("%Y/%m/%d %H:%M:%S", timeArray)
# # print otherStyleTime  # 2013/10/10 23:40:00
#
# tss3 = "2013/10/10 23:40:00"
# timeArray = time.strptime(tss3, "%Y/%m/%d %H:%M:%S")
# otherStyleTime2 = time.strftime("%Y-%m-%d %H:%M:%S", timeArray)
# # print otherStyleTime2  # 2013-10-10 23:40:00
#
#
# # python 字符串和时间格式(datetime)相互转换-
# # https://www.cnblogs.com/jfl-xx/p/8024596.html
# # https://www.cnblogs.com/xyao1/p/11053279.html
#

