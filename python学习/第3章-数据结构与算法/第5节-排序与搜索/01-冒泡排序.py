# coding:utf-8
# author:YJ沛


'''
稳定性： 1，维持次序  （稳定）
        2，次序被改变 （不稳定）

冒泡排序法稳定性： 稳定

最优时间复杂度：O(n) （表示遍历一次发现没有任何可以交换的元素，排序结束。）
最坏时间复杂度：O(n^2)


'''


a = [12, 3, 4, 5, 56, 234, 678, 7, 9, 89, 55, 4, 23, 1, 2, 5, 0, 3]

# 方法一：
print("# 方法一：")


def bubble_sort(item):
    '''冒泡排序'''
    for i in range(len(item) - 1):
        # 要遍历 len(item)-1 次数
        flag = False
        for num in range(len(item) - 1 - i):
            # 每次遍历都要比较 len(item)-1-i 次
            if item[num] > item[num + 1]:
                item[num], item[num + 1] = item[num + 1], item[num]
                flag = True
        if flag:
            '''为空表示没有进行数据交换，所以数据本身就是按顺序排序'''
            break


print(a)
bubble_sort(a)
print(a)


b = [12, 3, 4, 5, 56, 234, 678, 7, 9, 89, 55, 4, 23, 1, 2, 1, 2, 3]

# 方法二：
print("# 方法二：")


def bubble_sort2(item):
    for j in range(len(b) - 1, 0, -1):
        flag = False
        for i in range(j):
            if item[i] > item[i + 1]:
                item[i], item[i + 1] = item[i + 1], item[i]
                flag = True
        if flag:
            '''为空表示没有进行数据交换，所以数据本身就是按顺序排序'''
            break


print(b)
bubble_sort(b)
print(b)


'''
官方文档
def bubble_sort(alist):
    for j in range(len(alist)-1,0,-1):
        # j表示每次遍历需要比较的次数，是逐渐减小的
        for i in range(j):
            if alist[i] > alist[i+1]:
                alist[i], alist[i+1] = alist[i+1], alist[i]

li = [54,26,93,17,77,31,44,55,20]
bubble_sort(li)
print(li)
'''