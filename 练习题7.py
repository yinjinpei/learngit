# coding:utf-8

import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler

sched = BackgroundScheduler()
sched.start()


def job():
    print('执行一次任务')


MyJobID=datetime.now().strftime("%Y%m%d%H%M%S")

sched.add_job(job, 'interval',id=MyJobID, minutes=1,next_run_time=datetime.now(), start_date='2020-10-26 22:12:11', end_date='2020-11-11 23:00:00')

time.sleep(300)