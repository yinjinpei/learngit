# coding:utf-8
# author:YJ沛

from apscheduler.schedulers.background import BackgroundScheduler
import time

def job():
    print('job 2s')


if __name__=='__main__':

    sched = BackgroundScheduler(timezone='MST')

    # 三个参数分别为:函数、线程id、执行时间间隔
    sched.add_job(job, 'interval', id='3_second_job', seconds=2)
    sched.start()

    while(True):
        print('main 1s')
        time.sleep(1)

from apscheduler.schedulers.background import BackgroundScheduler
import datetime


def aps_test():
    print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), '你好')


scheduler = BackgroundScheduler()
scheduler.add_job(func=aps_test, trigger='cron', second='*/5')
scheduler.start()