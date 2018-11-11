# coding:utf-8
# author:YJ沛


# 如a+b+c=1000, 且a^2+b^2=c^2(a, b, c)为自然数, 如何求得所有a, b, c组合？

# 方法一：枚举法
import time
# start_time = time.time()
# for a in range(0,1001):
#     for b in range(0,1001):
#         for c in range(0,1001):
#             if a+b+c==1000 and a**2+b**2==c**2:
#                 print("a:%d, b:%d, c:%d "%(a,b,c))
# end_time = time.time()
# finished_time = end_time - start_time
# print("完成！")


# 方法二
start_time = time.time()
for a in range(0, 1001):
    for b in range(0, 1001):
        c = 1000 - a - b
        if a**2+b**2 == c**2:
            print("a:%d, b:%d, c:%d " % (a, b, c))

end_time = time.time()
finished_time = end_time - start_time
print("finished: %0.2f" % finished_time)


'''
1,时间复杂度与“大O记法”

2,常见时间复杂度

执行次数函数举例	阶	        非正式术语
12	            O(1)	    常数阶
2n+3	        O(n)	    线性阶
3n2+2n+1	    O(n2)	    平方阶
5log2n+20	    O(logn)	    对数阶 
2n+3nlog2n+19	O(nlogn)    nlogn阶
2n	            O(2n)	    指数阶
6n3+2n2+3n+4	O(n3)	    立方阶

3,所消耗的时间从小到大
O(1) < O(logn) < O(n) < O(nlogn) < O(n^2) < O(n^3) < O(2^n) < O(n!) < O(n^n)


'''