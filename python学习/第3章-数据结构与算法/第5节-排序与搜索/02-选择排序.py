# coding:utf-8
# author:YJ沛


'''
选择排序法稳定性： 不稳定（如果选择最大值放在最后结构，从小到大排序是不稳定的）

最优时间复杂度：O(n^2)
最坏时间复杂度：O(n^2)
'''
a = [12, 34, 5, 6, 7, 11, 12, 45, 57, 56, 6, 4, 2]


def select_sort(alist):
    '''选择排序'''
    n = len(alist)
    for j in range(n - 1):    # 0 ~ n-2
        min_index = j
        for i in range(j + 1, n):
            if alist[min_index] > alist[i]:  # 从小到大排序
                min_index = i
        alist[j], alist[min_index] = alist[min_index], alist[j]


print(a)
select_sort(a)
print(a)


a = [12, 34, 5, 6, 7, 11, 12, 45, 57, 56, 6, 4, 2]


def select_sort(alist):
    '''选择排序'''
    n = len(alist)
    for j in range(n - 1):    # 0 ~ n-2
        min_index = j
        for i in range(j + 1, n):
            if alist[min_index] < alist[i]:  # 从大到小排序
                min_index = i
        alist[j], alist[min_index] = alist[min_index], alist[j]


print(a)
select_sort(a)
print(a)


'''
官方文档
def selection_sort(alist):
    n = len(alist)
    # 需要进行n-1次选择操作
    for i in range(n-1):
        # 记录最小位置
        min_index = i
        # 从i+1位置到末尾选择出最小数据
        for j in range(i+1, n):
            if alist[j] < alist[min_index]:
                min_index = j
        # 如果选择出的数据不在正确位置，进行交换
        if min_index != i:
            alist[i], alist[min_index] = alist[min_index], alist[i]

alist = [54,226,93,17,77,31,44,55,20]
selection_sort(alist)
print(alist)
'''