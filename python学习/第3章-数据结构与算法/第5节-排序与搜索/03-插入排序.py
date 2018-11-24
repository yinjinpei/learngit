# coding:utf-8
# author:YJ沛


'''
插入排序法稳定性： 稳定

最优时间复杂度：O(n)
最坏时间复杂度：O(n^2)
'''

a = [12, 34, 7, 11, 12, 12, 56, 6, 4, 2]


def insert_sort(alist):
    '''选择排序'''

    n = len(alist)

    # 从右边的无序序列中取出多少个元素执行这样的过程
    for j in range(1, n):  # 0 ~ n-1
        i = j   # i 表示内层循环的起始值

        # 执行从右边的无序序列中取出第一个元素，即i位置的元素，然后将其插入到前端的正确位置中
        while i > 0:    # 相当range(j, 0, -1)
            if alist[i] < alist[i - 1]:  # 从小到大排序
                alist[i], alist[i - 1] = alist[i - 1], alist[i]
                i -= 1
            else:
                break
            print(alist)  # for test
    print(alist)

insert_sort(a)

b = [1,2,4,5,6,7,8]

insert_sort(b)


'''
官方文档
def insert_sort(alist):
    # 从第二个位置，即下标为1的元素开始向前插入
    for i in range(1, len(alist)):
        # 从第i个元素开始向前比较，如果小于前一个元素，交换位置
        for j in range(i, 0, -1):
            if alist[j] < alist[j-1]:
                alist[j], alist[j-1] = alist[j-1], alist[j]

alist = [54,26,93,17,77,31,44,55,20]
insert_sort(alist)
print(alist)
'''