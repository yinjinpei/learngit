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

time.sleep(300)