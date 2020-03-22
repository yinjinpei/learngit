# coding:utf-8
# author:YJ沛


import time
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.schedulers.background import BackgroundScheduler



sched = BackgroundScheduler()
# 添加作业，方法一：通过scheduled_job()修饰器来修饰函数
# @sched.scheduled_job('interval', seconds=5)
def my_job(hh):
    print(time.strftime('%Y-%m-%d %H:%M:%S'),hh)

# 添加作业，方法二：通过add_job()来添加作业
# sched.add_job(my_job, 'interval', seconds=2)
# sched.start()
#
# while True:
#     print('111')
#     time.sleep(2)

# 移除作业

# 单个任务
# job = sched.add_job(my_job, 'interval', minutesminutes=2)
# job.remove()

# 如果有多个任务序列的话可以给每个任务设置ID号，可以根据ID号选择清除对象，且remove放到start前才有效
# sched.add_job(my_job, 'interval', seconds=2, id='my_job_id')
# sched.remove_job('my_job_id')

sched.add_job(my_job, 'cron', year=2020,month = 3,day = 23,hour = 2,minute = 0,second = 0,args=['123'])
# sched.add_job(func=my_job,trigger='cron', day_of_week='mon-fri', hour=1, minute=29, end_date='2020-3-23')
print(1111111111)
sched.start()
print(2222222222222)

while True:
        print('11')
        time.sleep(1)
