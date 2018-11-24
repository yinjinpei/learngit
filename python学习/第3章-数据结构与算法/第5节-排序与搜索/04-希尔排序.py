# coding:utf-8
# author:YJ沛


'''
插入排序法稳定性： 不稳定

最优时间复杂度：根据步长序列的不同而不同
最坏时间复杂度：O(n^2)
'''

a = [12, 34, 7, 11, 12, 12, 56, 6, 4, 2]


def shell_sort(alist):
    '''希尔排序'''
    n = len(alist)
    gap = n // 2

    # gap变化到0之前，插入算法执行的次数
    while gap > 0:
        # 插入算法，与普通的插入算法的区别就是gap步长
        for j in range(gap, n):  # gap ~ n-1
            i = j   # j = [gap, gap+1, gap+2, ... , n-1]
            while i > 0:
                if alist[i] < alist[i - gap]:  # 从小到大排序
                    alist[i], alist[i - gap] = alist[i - gap], alist[i]
                    i -= gap
                else:
                    break
                print(alist)  # for test
        # 缩短gap步长
        gap //= 2
    print(alist)


shell_sort(a)


'''
官方文档
def shell_sort(alist):
    n = len(alist)
    # 初始步长
    gap = n / 2
    while gap > 0:
        # 按步长进行插入排序
        for i in range(gap, n):
            j = i
            # 插入排序
            while j>=gap and alist[j-gap] > alist[j]:
                alist[j-gap], alist[j] = alist[j], alist[j-gap]
                j -= gap
        # 得到新的步长
        gap = gap / 2

alist = [54,26,93,17,77,31,44,55,20]
shell_sort(alist)
print(alist)
'''
