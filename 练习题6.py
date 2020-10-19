from threading import Thread
import time
import random

SR_list=[]
def get_gitlab_SR():
    global SR_list
    time.sleep(random.randint(1,5))
    SR_list.append(random.randint(1,100))
    print('线程SR_list值：',SR_list)



thread_list=[]
for i in range(5):
    t=Thread(target=get_gitlab_SR)
    t.start()
    print(t)
    thread_list.append(t)


for thread in thread_list:
    thread.join()

print('汇总：',SR_list)



